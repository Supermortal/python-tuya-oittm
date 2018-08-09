"""
Module for encoding/decoding/hashing helper methods
"""
from base64 import (standard_b64encode, standard_b64decode)
from hashlib import md5
from .aescipher import AESCipher


def encode(key, msg, base64=True):
    """
    Convience wrapper around AESCipher encrypt method
    """
    pwd = key

    cipher = AESCipher(pwd)
    cipher_text = cipher.encrypt(msg)

    if base64 is True:
        b64_encoded_string = standard_b64encode(cipher_text)
        return b64_encoded_string.decode('UTF-8')

    return cipher_text


def decode(key, enc_msg, base64=True):
    """
    Convience wrapper around AESCipher decrypt method
    """
    pwd = key

    if base64 is True:
        enc_msg = standard_b64decode(enc_msg)

    cipher = AESCipher(pwd)
    plain_text = cipher.decrypt(enc_msg)

    return plain_text


def cipher_hash(msg):
    """
    Tuya-specific MD5 hash
    """
    msg = msg.encode('UTF-8')
    hashed_str = md5(msg)
    digest = hashed_str.digest()
    hex_str = digest.hex()
    return_str = hex_str.lower()[8:24]
    return return_str
