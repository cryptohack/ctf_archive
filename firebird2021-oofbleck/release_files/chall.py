import re
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from secret import flag

def encrypt(message, key):
    iv = os.urandom(16)
    cipher = AES.new(iv, AES.MODE_OFB, key)
    message = pad(message, 16)
    ciphertext = iv + cipher.encrypt(message)
    return ciphertext

def decrypt(ciphertext, key):
    iv, ciphertext = ciphertext[:16], ciphertext[16:]
    cipher = AES.new(iv, AES.MODE_OFB, key)
    message = cipher.decrypt(ciphertext)
    return unpad(message, 16)

if __name__ == '__main__':
    key = os.urandom(16)
    assert re.match(r'^firebird\{\w{58}\}$', flag)

    ciphertext = encrypt(flag.encode(), key)
    assert decrypt(ciphertext, key) == flag.encode()
    print(base64.b64encode(ciphertext).decode())
