import hashlib
import os
import random
import string

colors = ['\033[94m', '\033[96m', '\033[95m']
reset = '\033[0m'

banner = ''.join(random.choice(colors) + char + reset if char != ' ' else char for char in open("banner.txt", "r").read())


colors = ["\033[0;32m", "\033[0;33m", "\033[0;34m", "\033[0;35m", "\033[0;36m", "\033[0;37m", "\033[0;31m", "\033[38;5;248m", "\033[0m"]
green, yellow, blue, purple, cyan, white, red, grey, reset = colors

flag = ""

for c in open("flag.txt", "r").read(): flag += colors[random.randrange(0, 6)] + c
flag += reset

def PoW(bits):
	print(banner)
	n = random.randrange(0, 2**bits)
	a = "".join(random.choices(string.ascii_letters, k=20)).encode()
	hsh = hashlib.md5(str(n).encode() + a).digest()

	print(f"md5(str(n).encode() + {a}).hexdigest() = {bytes.hex(hsh)}")
	if int(input(f"Input the decimal result of n within range(2**{bits}): ")) != n:
		exit()
