"""
implementation of https://www.cs.umd.edu/~gasarch/TOPICS/miscrypto/rabinwithrecip.pdf
"""
import os
import random
import signal
from dataclasses import dataclass
from math import gcd
from typing import List, Tuple

import gmpy2
from Crypto.Util.number import bytes_to_long, getPrime


@dataclass
class Pubkey:
    n: int
    c: int


@dataclass
class Privkey:
    p: int
    q: int


@dataclass
class Enc:
    r: int
    s: int
    t: int

    def __repr__(self) -> str:
        return f"r = {self.r}\ns = {self.s}\nt = {self.t}"


def crt(r1: int, n1: int, r2: int, n2: int) -> int:
    g, x, y = gmpy2.gcdext(n1, n2)
    assert g == 1
    return int((n1 * x * r2 + n2 * y * r1) % (n1 * n2))


def gen_prime(pbits: int) -> int:
    p = getPrime(pbits)
    while True:
        if p % 4 == 3:
            return p
        p = getPrime(pbits)


def genkey(pbits: int) -> Tuple[Pubkey, Privkey]:
    p, q = gen_prime(pbits), gen_prime(pbits)
    n = p * q
    c = random.randint(0, n - 1)
    while True:
        if gmpy2.jacobi(c, p) == -1 and gmpy2.jacobi(c, q) == -1:
            break
        c = random.randint(0, n - 1)
    pubkey = Pubkey(n=n, c=c)
    privkey = Privkey(p=p, q=q)
    return pubkey, privkey


def encrypt(m: int, pub: Pubkey) -> Enc:
    assert 0 < m < pub.n
    assert gcd(m, pub.n) == 1
    r = int((m + pub.c * pow(m, -1, pub.n)) % pub.n)
    s = int(gmpy2.jacobi(m, pub.n))
    t = int(pub.c * pow(m, -1, pub.n) % pub.n < m)
    enc = Enc(r=r, s=s, t=t)
    assert s in [1, -1]
    assert t in [0, 1]
    return enc


def solve_quad(r: int, c: int, p: int) -> Tuple[int, int]:
    """
    Solve x^2 - r * x + c = 0 mod p
    See chapter 5.
    """

    def mod(poly: List[int]) -> None:
        """
        Calculate mod x^2 - r * x + c (inplace)
        """
        assert len(poly) == 3
        if poly[2] == 0:
            return
        poly[1] += poly[2] * r
        poly[1] %= p
        poly[0] -= poly[2] * c
        poly[0] %= p
        poly[2] = 0

    def prod(poly1: List[int], poly2: List[int]) -> List[int]:
        """
        Calculate poly1 * poly2 mod x^2 - r * x + c
        """
        assert len(poly1) == 3 and len(poly2) == 3
        assert poly1[2] == 0 and poly2[2] == 0
        res = [
            poly1[0] * poly2[0] % p,
            (poly1[1] * poly2[0] + poly1[0] * poly2[1]) % p,
            poly1[1] * poly2[1] % p,
        ]
        mod(res)
        assert res[2] == 0
        return res

    # calculate x^exp mod (x^2 - r * x + c) in GF(p)
    exp = (p - 1) // 2
    res_poly = [1, 0, 0]  # = 1
    cur_poly = [0, 1, 0]  # = x
    while True:
        if exp % 2 == 1:
            res_poly = prod(res_poly, cur_poly)
        exp //= 2
        if exp == 0:
            break
        cur_poly = prod(cur_poly, cur_poly)

    # I think the last equation in chapter 5 should be x^{(p-1)/2}-1 mod (x^2 - Ex + c)
    # (This change is not related to vulnerability as far as I know)
    a1 = -(res_poly[0] - 1) * pow(res_poly[1], -1, p) % p
    a2 = (r - a1) % p
    return a1, a2


def decrypt(enc: Enc, pub: Pubkey, priv: Privkey) -> int:
    assert 0 <= enc.r < pub.n
    assert enc.s in [1, -1]
    assert enc.t in [0, 1]
    mps = solve_quad(enc.r, pub.c, priv.p)
    mqs = solve_quad(enc.r, pub.c, priv.q)
    ms = []
    for mp in mps:
        for mq in mqs:
            m = crt(mp, priv.p, mq, priv.q)
            if gmpy2.jacobi(m, pub.n) == enc.s:
                ms.append(m)
    assert len(ms) == 2
    m1, m2 = ms
    if m1 < m2:
        m1, m2 = m2, m1
    if enc.t == 1:
        m = m1
    elif enc.t == 0:
        m = m2
    else:
        raise ValueError
    return m


if __name__ == "__main__":
    signal.alarm(300)
    flag = os.environ.get("FLAG", "FAKEFLAG{THIS_IS_FAKE}").encode()
    pbits = 1024
    pub, priv = genkey(pbits)
    while len(flag) < 255:
        flag += os.urandom(1)
    enc_flag = encrypt(bytes_to_long(flag), pub)
    print("encrypted flag:")
    print(enc_flag)
    while True:
        try:
            r, s, t = map(int, input("r, s, t = ").split(","))
            enc = Enc(r=r, s=s, t=t)
            enc_dec_enc = encrypt(decrypt(enc, pub, priv), pub)
            print("decrypt(encrypt(input)):")
            print(enc_dec_enc)
        except KeyboardInterrupt:
            break
        except Exception:
            print("Something wrong...")
