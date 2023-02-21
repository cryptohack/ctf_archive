import os
import signal
from hashlib import sha256
from random import SystemRandom

from Crypto.Util.number import bytes_to_long, long_to_bytes

random = SystemRandom()

q = 8383489
b = 16383
w = 3
PR = PolynomialRing(Zmod(q), name="x")
x = PR.gens()[0]
n = 420
phi = x**n - 1
Rq = PR.quotient(phi, "x")
x = Rq.gens()[0]


def sample(K):
    poly = 0
    for i in range(n):
        poly += random.randint(-K, K) * x**i
    return poly


def polyhash(poly, m):
    h = sha256()
    for i in range(n):
        h.update(long_to_bytes(int(poly[i]), 3))
    h.update(m)
    return h.digest()


def hash2poly(h):
    hash_int = bytes_to_long(h)
    poly = 0
    for i in range(n):
        poly += ((1 << i) & hash_int != 0) * x**i
    return poly


def keygen(a):
    s = sample(1)
    e = sample(1)
    t = a * s + e
    r = (s, e)
    return r, t


def sign(m, r, t, a):
    s, e = r
    while True:
        y1 = sample(b)
        y2 = sample(b)
        c_ = polyhash(a * y1 + y2, m)
        c = hash2poly(c_)
        z1 = s * c + y1
        z2 = e * c + y2
        valid = True
        for i in range(n):
            if b - w < z1[i] < q - (b - w) or b - w < z2[i] < q - (b - w):
                valid = False
                break
        if valid:
            break
    return z1, z2, c


def verify(m, sig, t, a):
    z1, z2, c = sig
    for i in range(n):
        if min(z1[i], q - z1[i]) > b - w:
            return False
        if min(z2[i], q - z2[i]) > b - w:
            return False
    d_ = polyhash(a * z1 + z2 - t * c, m)
    d = hash2poly(d_)
    return d == c


def encode_poly(poly):
    enc = b""
    for i in range(n):
        enc += long_to_bytes(int(poly[i]), 3)
    return enc


def decode_poly(poly_enc):
    assert len(poly_enc) == 3 * n
    poly = 0
    for i in range(0, 3 * n, 3):
        poly += bytes_to_long(poly_enc[i: i+3]) * x ** (i // 3)
    return poly


if __name__ == "__main__":
    signal.alarm(600)
    flag = os.environ.get("FLAG", "FAKEFLAG{THIS_IS_FAKE}")
    a = sample((q - 1) // 2)
    r, t = keygen(a)
    a_enc = encode_poly(a)
    t_enc = encode_poly(t)
    print(f"a_enc = {a_enc.hex()}")
    print(f"t_enc = {t_enc.hex()}")
    z1 = decode_poly(bytes.fromhex(input("z1 = ")))
    z2 = decode_poly(bytes.fromhex(input("z2 = ")))
    c = decode_poly(bytes.fromhex(input("c = ")))
    m = b"sign me!"
    if verify(m, (z1, z2, c), t, a):
        print(f"{flag = }")
    else:
        print("try harder...")
