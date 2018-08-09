import unittest
from python_tuya_oittm.helpers.message_parser import MessageParser


class TestTuyaMessageParserMethods(unittest.TestCase):

    def test_json(self):
        data = {}
        data['test'] = 'test'

        message_parser = MessageParser()
        jsonBytes = message_parser.to_json_bytes(data)

        self.assertIsNotNone(jsonBytes)

    def test_get_prefix(self):
        message_parser = MessageParser()
        prefixBytes = message_parser.get_prefix('get')

        self.assertEqual(
            prefixBytes, b'\x00\x00U\xaa\x00\x00\x00\x00\x00\x00\x00\n')

    def test_get_suffix(self):
        message_parser = MessageParser()
        suffixBytes = message_parser.get_suffix()

        self.assertEqual(suffixBytes, b'\x00\x00\xaaU')

    def test_get_crc32(self):
        message_parser = MessageParser()
        crc32Bytes = message_parser.get_crc32_buffer()

        self.assertEqual(crc32Bytes, b'\x00\x00\x00\x00')


if __name__ == '__main__':
    unittest.main()
