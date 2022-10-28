import re
from Crypto.Util import Counter
from Crypto.Cipher import AES
import os

# (Obseleted - This was a comment in HKCERT CTF 2020. Please delete this.)
# In the future, we have not only time inversion but also quantum computers.
# So, we need to encrypt twice to double the key size.
#
# Mystiz: I just want to make a challenge as soon as possible. Let's do brainless copy and paste.
class TenetAES():
    def __init__(self, key):
        self.aes128_00 = AES.new(key=key[ 0: 1] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_01 = AES.new(key=key[ 1: 2] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_02 = AES.new(key=key[ 2: 3] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_03 = AES.new(key=key[ 3: 4] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_04 = AES.new(key=key[ 4: 5] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_05 = AES.new(key=key[ 5: 6] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_06 = AES.new(key=key[ 6: 7] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_07 = AES.new(key=key[ 7: 8] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_08 = AES.new(key=key[ 8: 9] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_09 = AES.new(key=key[ 9:10] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_10 = AES.new(key=key[10:11] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_11 = AES.new(key=key[11:12] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_12 = AES.new(key=key[12:13] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_13 = AES.new(key=key[13:14] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_14 = AES.new(key=key[14:15] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self.aes128_15 = AES.new(key=key[15:16] + b'\0'*15, mode=AES.MODE_CTR, counter=Counter.new(128, initial_value=0))

    def encrypt(self, s):
        s = self.aes128_00.encrypt(s)
        s = self.aes128_01.encrypt(s)
        s = self.aes128_02.encrypt(s)
        s = self.aes128_03.encrypt(s)
        s = self.aes128_04.encrypt(s)
        s = self.aes128_05.encrypt(s)
        s = self.aes128_06.encrypt(s)
        s = self.aes128_07.encrypt(s)
        s = self.aes128_08.encrypt(s)
        s = self.aes128_09.encrypt(s)
        s = self.aes128_10.encrypt(s)
        s = self.aes128_11.encrypt(s)
        s = self.aes128_12.encrypt(s)
        s = self.aes128_13.encrypt(s)
        s = self.aes128_14.encrypt(s)
        s = self.aes128_15.encrypt(s)
        return s

    def decrypt(self, data):
        s = self.aes128_15.decrypt(s)
        s = self.aes128_14.decrypt(s)
        s = self.aes128_13.decrypt(s)
        s = self.aes128_12.decrypt(s)
        s = self.aes128_11.decrypt(s)
        s = self.aes128_10.decrypt(s)
        s = self.aes128_09.decrypt(s)
        s = self.aes128_08.decrypt(s)
        s = self.aes128_07.decrypt(s)
        s = self.aes128_06.decrypt(s)
        s = self.aes128_05.decrypt(s)
        s = self.aes128_04.decrypt(s)
        s = self.aes128_03.decrypt(s)
        s = self.aes128_02.decrypt(s)
        s = self.aes128_01.decrypt(s)
        s = self.aes128_00.decrypt(s)
        return s

def main():
    with open('flag.txt', 'r') as f:
        flag = f.read()

    assert re.match(r'hkcert21\{\w{35}\}', flag)

    message = f'Congratulations! {flag}'.encode()

    key = os.urandom(16)

    cipher = TenetAES(key)
    ciphertext = cipher.encrypt(message).hex()
    print(ciphertext)

if __name__ == '__main__':
    main()