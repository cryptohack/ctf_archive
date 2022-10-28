import random
import gmpy2

e = 0x10001

with open('flag.txt', 'rb') as f:
    m = f.read()
    m = int.from_bytes(m, 'big')

while True:
    p = random.getrandbits(256)
    q = int(gmpy2.digits(p, 3))

    # Ensure that they are prime
    if not gmpy2.is_prime(p): continue
    if not gmpy2.is_prime(q): continue

    # Ensure that d exists
    if (p-1) % e == 0: continue
    if (q-1) % e == 0: continue

    break

n = p * q
assert 0 <= m < n

c = pow(m, e, n)

print(f'{n = }')
print(f'{e = }')
print(f'{c = }')