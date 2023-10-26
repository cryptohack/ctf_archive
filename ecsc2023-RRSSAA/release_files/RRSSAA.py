from math import prod
from secrets import randbelow
import random
from Crypto.Util.number import *

def get_prime(n):
    p = 1
    r = random.Random()
    r.seed(randbelow(2**n))
    while not isPrime(p):
        p = r._randbelow(2**256) | 1
    return p

flag = open("flag.txt", "rb").read().strip()
assert len(flag) == 128
N = prod(get_prime(i) for i in range(2, len(flag)))
print(hex(N), hex(pow(bytes_to_long(flag), 0x10001, N)))
