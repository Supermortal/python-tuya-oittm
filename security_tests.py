import unittest
from python_tuya_oittm.security.aescipher import AESCipher
from python_tuya_oittm.security.cipher import (encode, decode, cipher_hash)


class TestTuyaSecurityMethods(unittest.TestCase):
    def test_aes_encryption(self):
        msg = 'test'
        pwd = 'testpasswordthin'

        cipher = AESCipher(pwd)
        cipherText = cipher.encrypt(msg)

        self.assertEqual(
            cipherText, b'H\x10\xa2\xf7\xc2\xe7]W\x0f\xbc\xa9\x9e\xc1|\xc5\x03')

    def test_aes_decyrption(self):
        encryptedMsg = b'H\x10\xa2\xf7\xc2\xe7]W\x0f\xbc\xa9\x9e\xc1|\xc5\x03'
        pwd = 'testpasswordthin'

        cipher = AESCipher(pwd)
        decryptedText = cipher.decrypt(encryptedMsg)

        self.assertEqual(
            decryptedText, 'test')

    def test_security_encode(self):
        key = 'testpasswordthin'
        cipherText = encode(key, 'test', False)

        self.assertEqual(
            cipherText, b'H\x10\xa2\xf7\xc2\xe7]W\x0f\xbc\xa9\x9e\xc1|\xc5\x03')

    def test_security_decode(self):
        key = 'testpasswordthin'
        decryptedText = decode(
            key, b'H\x10\xa2\xf7\xc2\xe7]W\x0f\xbc\xa9\x9e\xc1|\xc5\x03', False)

        self.assertEqual(
            decryptedText, 'test')

    def test_hash(self):
        msg = 'test'
        cipherText = cipher_hash(msg)

        self.assertEqual(
            cipherText, '4621d373cade4e83')


if __name__ == '__main__':
    unittest.main()
