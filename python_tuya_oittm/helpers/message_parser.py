"""
Module for MessageParser class
"""
import json
import struct

GET_COMMAND_BYTE = '0a'
SET_COMMAND_BYTE = '07'


class MessageParser:
    """
    Class for parsing Tuya messages
    """

    def to_json_bytes(self, data, sort=True):
        """
        Takes a dictionary/object, and turns it into JSON bytes
        (removes all white space in JSON string)
        """
        json_str = json.dumps(data, sort_keys=sort).replace(" ", "")
        json_bytes = json_str.encode('UTF-8')
        return json_bytes

    def get_prefix(self, command_type):
        """
        Get magic prefix bytes with added command byte based on command type
        """
        if command_type == 'get':
            prefix = '000055aa00000000000000{GET_COMMAND_BYTE}'.format(
                GET_COMMAND_BYTE=GET_COMMAND_BYTE)
        else:
            prefix = '000055aa00000000000000{SET_COMMAND_BYTE}'.format(
                SET_COMMAND_BYTE=SET_COMMAND_BYTE)

        prefix_bytes = bytes.fromhex(prefix)
        return prefix_bytes

    def get_suffix(self):
        """
        Get magic suffix bytes
        """
        suffix = '0000aa55'
        suffix_bytes = bytes.fromhex(suffix)
        return suffix_bytes

    def get_crc32_buffer(self):
        """
        Get crc32 buffer bytes (just 0's for now)
        """
        crc32 = '00000000'
        crc32_bytes = bytes.fromhex(crc32)
        return crc32_bytes

    def _encode(self, payload, command_type):
        """
        Encode entire packet to be sent to local Tuya device; takes a dictionary/object
        """
        crc32_buffer = self.get_crc32_buffer()
        suffix = self.get_suffix()
        init_list = (payload + crc32_buffer + suffix)
        init_list_len = len(init_list)
        init_list_len_bytes = init_list_len.to_bytes(4, byteorder='big')

        prefix = self.get_prefix(command_type)
        byte_arr = prefix + init_list_len_bytes + payload + crc32_buffer + suffix

        return bytearray(byte_arr)

    def encode(self, data, command_type='get'):
        """
        Encode entire packet to be sent to local Tuya device; takes a dictionary/object
        """
        payload = self.to_json_bytes(data, False)
        return self._encode(payload, command_type)

    def encode_bytes(self, data, command_type='get'):
        """
        Encode entire packet to be sent to local Tuya device; takes bytes as an argument
        """
        payload = data
        return self._encode(payload, command_type)

    def parse(self, data):
        """
        Parse a received response from a local Tuya device and return the payload
        """
        data_length = len(data)

        if data_length < 16:
            return False

        prefix = struct.unpack('>I', data[0:4])
        prefix = hex(prefix[0])

        if prefix != '0x55aa':
            return False

        suffix = struct.unpack(
            '>I', data[data_length - 4:data_length])
        suffix = hex(suffix[0])

        if suffix != '0xaa55':
            return False

        payload = data[20:data_length]
        payload_length = len(payload)

        if len(data) - 8 < payload_length:
            return False

        payload_data = data[0:data_length - 8]

        payload_data_len = len(payload_data)
        payload_data = payload_data[payload_data_len -
                                    payload_length + 8:payload_data_len]

        return payload_data.decode('UTF-8')
