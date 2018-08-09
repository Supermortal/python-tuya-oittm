import unittest
from python_tuya_oittm import TuyaClient, OittmHumidifierClient

TEST_DEVICE_ID = '<enter a device id>'
TEST_ENCRYPTION_KEY = '<enter an encryption key>'


class TestTuyaClientIntegrationMethods(unittest.TestCase):

    def test_device_discovery(self):
        tuya_client = TuyaClient()
        discovered_devices = tuya_client.discover_devices(5)
        self.assertIsNotNone(discovered_devices)

    def test_device_get_status(self):
        tuya_client = OittmHumidifierClient()
        device_status = tuya_client.get_device_status(TEST_DEVICE_ID)
        self.assertIsNone(device_status)

    def test_device_set_status(self):
        tuya_client = OittmHumidifierClient()
        device_updated = tuya_client.set_device_status(
            'Fog Level', '2', TEST_DEVICE_ID, TEST_ENCRYPTION_KEY)
        self.assertTrue(device_updated)


if __name__ == '__main__':
    unittest.main()
