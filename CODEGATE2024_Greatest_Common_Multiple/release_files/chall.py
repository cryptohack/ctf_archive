from Crypto.Cipher import AES
from os import urandom
from signal import alarm
from secret import PoW, flag

PoW(26)
alarm(20)

gen = lambda: urandom(12)
randbit = lambda: gen()[0] & 1

key, nonce = urandom(16), gen()

new = lambda: AES.new(key, AES.MODE_GCM, nonce)
s = [gen(), gen()]

while cmd := input("> "):
	if cmd == "tag":
		cipher = new()
		cipher.update(s[0])
		cipher.encrypt(s[1])
		print(f"tag: {cipher.digest().hex()}")

	elif cmd == "u1":
		s[randbit()] = gen()

	elif cmd == "u2":
		s[randbit()] += gen()

if input(f"tag: ") == new().digest().hex():
	print(flag)
