"""
Main pytuya-redux module
"""
from threading import Lock
import logging
import time
from .device_maps import (create_reverse_device_map, oittm)
from .api_client import ApiClient

name = "python-tuya-oittm"


SLEEP_ON_FAILURE_SECONDS = 5
LOCK = Lock()
LOG = logging.getLogger(__name__)


class TuyaClient:
    """
    Tuya client for interfacing with Tuya devices over a local network
    Currently supported device_types:
    oittm-humidifer
    """

    def __init__(self, device_map=None, max_retries=3):
        """
        Initialize class
        """
        self.device_map = device_map
        self.rev_device_map = None
        if device_map is not None:
            self.rev_device_map = create_reverse_device_map(self.device_map)
        self.max_retries = max_retries

    def discover_devices(self, max_attempts=15):
        """
        Discover Tuya devices on the local network
        """
        api_client = ApiClient()
        data = api_client.get_metadata(None, max_attempts, True)
        return data

    def _user_friendly_status_mapping(self, raw_device_status):
        """
        Map raw numerical device statuses to user friendly string names
        """
        if self.device_map is None:
            return raw_device_status
        if 'dps' not in raw_device_status:
            return None

        device_status = {}
        for key, value in raw_device_status['dps'].items():
            if key in self.device_map:
                device_status[self.device_map[key]] = value
            else:
                device_status[key] = value

        return device_status

    def get_device_metadata(self, device_id):
        """
        Get the metadata of a Tuya device on the local network.
        This information includes local encryption key and
        IP address
        """
        api_client = ApiClient()

        for _ in range(0, self.max_retries):
            LOCK.acquire()
            try:
                device_metadata = api_client.get_metadata(device_id)
            except:
                time.sleep(SLEEP_ON_FAILURE_SECONDS)
                continue
            finally:
                LOCK.release()

            if device_metadata is not None:
                return device_metadata
            else:
                time.sleep(SLEEP_ON_FAILURE_SECONDS)

        return None

    def get_device_status(self, device_id, ip_address=None):
        """
        Get the status of a Tuya device on the local network;
        if ip_address is set to None, this method will attempt
        to use the ip_address returned from device metadata
        """
        api_client = ApiClient()

        if ip_address is None:
            for _ in range(0, self.max_retries):
                LOCK.acquire()
                try:
                    metadata = api_client.get_metadata(device_id=device_id)
                except:
                    time.sleep(SLEEP_ON_FAILURE_SECONDS)
                    continue
                finally:
                    LOCK.release()

                if metadata is not None:
                    ip_address = metadata['ip']
                    break
                else:
                    time.sleep(SLEEP_ON_FAILURE_SECONDS)

        if ip_address is None:
            return None

        for _ in range(0, self.max_retries):
            LOCK.acquire()
            try:
                raw_device_status = api_client.get_status(
                    ip_address, device_id)
            except:
                time.sleep(SLEEP_ON_FAILURE_SECONDS)
                continue
            finally:
                LOCK.release()

            if raw_device_status is not None:
                device_status = self._user_friendly_status_mapping(
                    raw_device_status)
                return device_status
            else:
                time.sleep(SLEEP_ON_FAILURE_SECONDS)

        return None

    def set_device_status(self, update_key, update_value, device_id, encryption_key=None, ip_address=None, version=3.1):
        """
        Set the status of a Tuya device on the local network;
        if encryption_key is set to None, this method will attempt
        to use the local key returned with device metadata,
        if ip_address is set to None, this method will also attempt
        to use the ip_address returned in device metadata
        """
        api_client = ApiClient()

        dps = None
        if self.rev_device_map is not None:
            dps = {'dps': self.rev_device_map[update_key], 'set': update_value}
        else:
            dps = {'dps': update_key, 'set': update_value}

        if ip_address is None or encryption_key is None:
            for _ in range(0, self.max_retries):
                LOCK.acquire()
                try:
                    metadata = api_client.get_metadata(device_id=device_id)
                except:
                    time.sleep(SLEEP_ON_FAILURE_SECONDS)
                    continue
                finally:
                    LOCK.release()

                if metadata is not None and any(metadata) is not False:
                    if ip_address is None:
                        ip_address = metadata['ip']
                    if encryption_key is None and any(metadata) is not False:
                        encryption_key = metadata['productKey']
                    break
                else:
                    time.sleep(SLEEP_ON_FAILURE_SECONDS)

        device_updated = False
        for _ in range(0, self.max_retries):
            LOCK.acquire()
            try:
                device_updated = api_client.set_status(
                    dps, ip_address, device_id, encryption_key, version)
            except:
                time.sleep(SLEEP_ON_FAILURE_SECONDS)
                continue
            finally:
                LOCK.release()

            if device_updated is True:
                break
            else:
                time.sleep(SLEEP_ON_FAILURE_SECONDS)

        return device_updated


class OittmHumidifierClient(TuyaClient):
    def __init__(self, max_retries=3):
        """
        Initialize class
        """
        TuyaClient.__init__(self, oittm.OITTM_HUMIDIFIER_MAP, max_retries)
