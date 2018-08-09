import unittest
from python_tuya_oittm import TuyaClient, OittmHumidifierClient


class TestTuyaClientMethods(unittest.TestCase):

    def test_device_map_is_set_when_device_provided(self):
        tuya_client = OittmHumidifierClient()
        self.assertEqual(tuya_client.device_map, {
                         '1': 'Power', '6': 'Fog Level', '11': 'LED Light', '101': 'Water Low', '12': 'Timer'})

    def test_device_map_is_none_when_no_device_provided(self):
        tuya_client = TuyaClient()
        self.assertIsNone(tuya_client.device_map)


if __name__ == '__main__':
    unittest.main()
