import unittest
from python_tuya_oittm.api_client import ApiClient

TEST_DEVICE_ID = '<enter a device id>'
TEST_ENCRYPTION_KEY = '<enter an encryption key>'


class TestTuyaApiClientIntegratedMethods(unittest.TestCase):

    def test_get_metadata(self):
        api_client = ApiClient()
        data = api_client.get_metadata()
        self.assertIsNotNone(data)

    def test_get_metadata_with_device_id(self):
        api_client = ApiClient()
        data = api_client.get_metadata(TEST_DEVICE_ID)
        self.assertIsNotNone(data)

    def test_get_metadata_with_bad_device_id(self):
        api_client = ApiClient()
        data = api_client.get_metadata('gibberish', 5)
        self.assertEqual(data, False)

    def test_get_metadata_with_discovery(self):
        api_client = ApiClient()
        data = api_client.get_metadata(None, 5, discover=True)
        self.assertIsNotNone(data)

    def test_get_status(self):
        api_client = ApiClient()
        metaData = api_client.get_metadata()
        status = api_client.get_status(metaData['ip'], metaData['gwId'])
        self.assertIsNotNone(status)

    def test_set_status(self):
        dps = {'dps': '6', 'set': '2'}

        api_client = ApiClient()
        metaData = api_client.get_metadata()
        result = api_client.set_status(
            dps, metaData['ip'], metaData['gwId'], TEST_ENCRYPTION_KEY)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
