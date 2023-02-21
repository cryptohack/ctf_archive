import os
from math import gcd

from Crypto.Util.number import bytes_to_long, isPrime

from secret import p, q, x1, y1, x2, y2, e

flag = os.environ.get("FLAG", "FAKEFLAG{THIS_IS_FAKE}").encode()

# properties of secret variables
assert isPrime(p) and p.bit_length() == 768
assert isPrime(q) and q.bit_length() == 768
assert isPrime(e) and e.bit_length() == 256
assert gcd((p - 1) * (q - 1), e) == 1
assert x1.bit_length() <= 768 and x2.bit_length() <= 768
assert y1.bit_length() <= 640 and y2.bit_length() <= 640
assert x1 ** 2 + e * y1 ** 2 == p * q
assert x2 ** 2 + e * y2 ** 2 == p * q

# encrypt flag by RSA, with xor
n = p * q
c = pow(bytes_to_long(flag) ^^ x1 ^^ y1 ^^ x2 ^^ y2, e, n)
print(f"{n = }")
print(f"{c = }")

# hints 🍣
F = RealField(1337)
x = vector(F, [x1, x2])
y = vector(F, [y1, y2])
# rotate
theta = F.random_element(min=-pi, max=pi)
R = matrix(F, [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
x = R * x
y = R * y
print(f"{x = }")
print(f"{y = }")
