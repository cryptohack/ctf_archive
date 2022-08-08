from Crypto.Util.number import getStrongPrime, inverse, long_to_bytes
import string, signal, random, hashlib, os
signal.alarm(300)

def gen_pow():
    print("Solve PoW plz")
    s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    print(s)
    answer = input()
    hash = hashlib.sha256((s + answer).encode()).hexdigest()
    if hash[:6] != "000000":
        exit() 

def mapped(s, perm):
    ret = ""
    for x in s:
        ret += perm[int(x, 16)]
    return ret

gen_pow()
e = 293
p, q = 0, 0
while True:
    p = getStrongPrime(1024)
    q = getStrongPrime(1024)
    if (p - 1) % e != 0 and (q - 1) % e != 0:
        break 

n = p * q 
d_p = inverse(e, p - 1)
d_q = inverse(e, q - 1)

perm = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
random.shuffle(perm)

print(n)
print(mapped(long_to_bytes(d_p, 128).hex(), perm))
print(mapped(long_to_bytes(d_q, 128).hex(), perm))

u = int(input())
v = int(input())

if 1 < u < n and 1 < v < n and u * v == n:
    flag = os.environ.get("FLAG")
    print(flag)
else:
    print("fail")
