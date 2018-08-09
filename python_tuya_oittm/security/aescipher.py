"""
Module for AESCipher class
"""
from Crypto.Cipher import AES

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes


def pad(string_to_pad):
    """
    Method that pads a message in preperation to be encrypted in AES
    """
    return string_to_pad + (BLOCK_SIZE - len(string_to_pad) % BLOCK_SIZE) * \
        chr(BLOCK_SIZE - len(string_to_pad) % BLOCK_SIZE)


def unpad(string_to_unpad):
    """
    Method that unpads after decryption
    """
    return string_to_unpad[:-ord(string_to_unpad[len(string_to_unpad) - 1:])]


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        """
        Initialize class
        """
        self.key = key.encode('UTF-8')

    def encrypt(self, raw):
        """
        Encrypt the message
        """
        raw = pad(raw).encode('UTF-8')
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        """
        Decrypt the message
        """
        # enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('UTF-8')
