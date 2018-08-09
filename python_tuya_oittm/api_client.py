"""
Api client for making local Tuya device requests
"""
import asyncio
import json
import time
import logging
from .helpers.message_parser import MessageParser
from .security.cipher import (encode, cipher_hash)

LOG = logging.getLogger(__name__)


def current_milli_time():
    """
    Get current time in milliseconds
    """
    return int(round(time.time() * 1000))


class TuyaGetMetadataProtocolFactory:
    """
    Protocol factory for getting metadata on local Tuya devices
    """

    def __init__(self):
        """
        Initialize class
        """
        self.device_id = None
        self.discover = False
        self.max_attempts = 15
        self.current_attempts = 0
        self.data = {}
        self.transport = None

    def get(self, device_id, max_attempts, discover):
        """
        Start waiting on the UDP socket for requests
        """
        self.device_id = device_id
        self.discover = discover
        self.max_attempts = max_attempts
        self.current_attempts = 0
        self.data = {}

        loop = asyncio.get_event_loop()

        listen = loop.create_datagram_endpoint(
            lambda: self, local_addr=('0.0.0.0', 6666))
        transport, protocol = loop.run_until_complete(listen)

        return transport

    def connection_made(self, transport):
        """
        Connection to UDP socket made
        """
        self.transport = transport

    def datagram_received(self, data, addr):
        """
        Datagram received on the UDP socket; parse response and check attempts against max attempts
        """
        self.current_attempts += 1
        message_parser = MessageParser()
        parsed_data = message_parser.parse(data)
        parsed_data_json_obj = json.loads(parsed_data)

        if self.current_attempts >= self.max_attempts:
            if any(self.data) is False:
                self.data = False
            self.transport.close()
            return

        if self.device_id is not None and parsed_data_json_obj['gwId'] != self.device_id:
            return

        if self.discover:
            if parsed_data_json_obj['gwId'] not in self.data:
                self.data[parsed_data_json_obj['gwId']] = parsed_data_json_obj
        else:
            self.data = parsed_data_json_obj
            self.transport.close()

    def error_received(self, exc):
        """
        On UDP error received
        """
        LOG.exception(exc)
        print('Error received:', exc)

    def connection_lost(self, exc):
        """
        UDP connection lost/closed
        """
        if exc is not None:
            LOG.exception(exc)
        loop = asyncio.get_event_loop()
        loop.stop()


class TuyaGetStatusProtocolFactory:
    """
    Protocol factory for getting the status of a local Tuya device
    """

    def __init__(self):
        """
        Initialize class
        """
        self.device_id = None
        self.payload_bytes = None
        self.transport = None
        self.data = None

    def get(self, ip_address, device_id):
        """
        Open TCP connection to the local Tuya device
        """
        self.device_id = device_id

        message_parser = MessageParser()

        payload = {'gwId': self.device_id, 'devId': self.device_id}
        self.payload_bytes = message_parser.encode(payload)

        loop = asyncio.get_event_loop()

        listen = loop.create_connection(lambda: self, ip_address, 6668)
        loop.run_until_complete(listen)

    def connection_made(self, transport):
        """
        On connected to local Tuya device
        """
        self.transport = transport
        self.transport.write(self.payload_bytes)

    def data_received(self, data):
        """
        Status response received from local Tuya device
        """
        message_parser = MessageParser()
        parsed_data = message_parser.parse(data)
        parsed_data_json_obj = json.loads(parsed_data)
        self.data = parsed_data_json_obj
        loop = asyncio.get_event_loop()
        loop.stop()

    def error_received(self, exc):
        """
        On error received
        """
        LOG.exception(exc)
        loop = asyncio.get_event_loop()
        loop.stop()

    def connection_lost(self, exc):
        """
        TCP connection lost/closed
        """
        if exc is not None:
            LOG.exception(exc)
        loop = asyncio.get_event_loop()
        loop.stop()


class TuyaSetStatusProtocolFactory:
    """
    Protocol factory for setting the status of a local Tuya device
    """

    def __init__(self):
        """
        Initialize class
        """
        self.message = None
        self.transport = None
        self.data = False

    def set(self, ip_address, message):
        """
        Open TCP connection to local Tuya device to set status
        """
        self.message = message

        loop = asyncio.get_event_loop()

        listen = loop.create_connection(lambda: self, ip_address, 6668)
        loop.run_until_complete(listen)

    def connection_made(self, transport):
        """
        TCP connection made to local Tuya device
        """
        self.transport = transport
        self.transport.write(self.message)

    def data_received(self, data):
        """
        Status has been set; a succesful response should be ''
        """
        message_parser = MessageParser()
        parsed_data = message_parser.parse(data)
        self.data = bool(parsed_data == '')

        loop = asyncio.get_event_loop()
        loop.stop()

    def error_received(self, exc):
        """
        On error received
        """
        LOG.exception(exc)
        loop = asyncio.get_event_loop()
        loop.stop()

    def connection_lost(self, exc):
        """
        TCP connection lost/closed
        """
        if exc is not None:
            LOG.exception(exc)
        loop = asyncio.get_event_loop()
        loop.stop()


class ApiClient:
    """
    Class for sending/receiving Tuya messages
    """

    def _get_timestamp(self):
        """
        Get timestamp in Tuya-expected format
        """
        return str(int(current_milli_time() / 1000))

    def _prepare_data(self, dps, device_id, key):
        """
        Prepare data for set status request
        """
        timestamp = self._get_timestamp()
        payload = {'devId': device_id, 'uid': '', 't': timestamp}

        set_dictionary = {dps['dps']: dps['set']}
        payload['dps'] = set_dictionary
        payload_json = json.dumps(payload).replace(" ", "")

        encoded_data = encode(key, payload_json, True)
        return encoded_data

    def get_metadata(self, device_id=None, max_attempts=15, discover=False):
        """
        Fetch metadata for local Tuya devices; can be used for a specific id,
         the first device found, or for generic discovery
        """
        loop = asyncio.get_event_loop()

        resolve = TuyaGetMetadataProtocolFactory()
        transport = resolve.get(device_id, max_attempts, discover)

        loop.run_forever()
        transport.close()

        return resolve.data

    def get_status(self, ip_address, device_id):
        """
        Gets the status of a local Tuya device
        """
        loop = asyncio.get_event_loop()

        resolve = TuyaGetStatusProtocolFactory()
        resolve.get(ip_address, device_id)

        loop.run_forever()

        return resolve.data

    def set_status(self, dps, ip_address, device_id, key, version=3.1):
        """
        Set the status of a local Tuya device; can only set on property at a time
        """

        encoded_data = self._prepare_data(dps, device_id, key)
        md5 = cipher_hash(f'data={encoded_data}||lpv={version}||{key}')
        data = f'{version}{md5}{encoded_data}'.encode('UTF-8')

        message_parser = MessageParser()
        message = message_parser.encode_bytes(data, 'set')

        resolve = TuyaSetStatusProtocolFactory()
        resolve.set(ip_address, message)

        loop = asyncio.get_event_loop()
        loop.run_forever()

        return resolve.data
