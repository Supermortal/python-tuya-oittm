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
        self.assertIsNotNone(device_status)

    def test_device_set_status(self):
        tuya_client = OittmHumidifierClient()
        device_updated = tuya_client.set_device_status(
            'Fog Level', '2', TEST_DEVICE_ID, TEST_ENCRYPTION_KEY)
        self.assertTrue(device_updated)

    def test_device_get_status_then_set_status_then_get_status(self):
        tuya_client = OittmHumidifierClient()

        device_metadata = tuya_client.get_device_metadata(TEST_DEVICE_ID)

        device_status = tuya_client.get_device_status(
            TEST_DEVICE_ID, device_metadata['ip'])
        self.assertIsNotNone(device_status)

        device_updated = tuya_client.set_device_status(
            'Fog Level', '2', TEST_DEVICE_ID, TEST_ENCRYPTION_KEY, device_metadata['ip'])
        self.assertTrue(device_updated)

        device_status = tuya_client.get_device_status(
            TEST_DEVICE_ID, device_metadata['ip'])
        self.assertIsNotNone(device_status)


if __name__ == '__main__':
    unittest.main()
