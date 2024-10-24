#!/usr/bin/env python3

import hashlib
import os
import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

flag = os.getenv('FLAG', 'ECSC{redacted}')

proof.all(False)

def rand(R, d = None):
    B = R.base_ring()
    if d is None:
        d = R.degree()
    if B is R:
        return R(secrets.randbits(R.cardinality().nbits() - 1))
    else:
        return R([rand(B) for _ in range(d)])


def tolist(pt):
    R = pt.parent()
    B = R.base_ring()
    if R is B:
        yield int(pt)
    else:
        for e in pt.list():
            yield from tolist(e)


def fromlist(R, xs, d=None):
    B = R.base_ring()
    if d is None:
        d = R.degree()
    if B is R:
        return R(next(xs))
    return R([fromlist(B, xs) for _ in range(d)])


def evalp(poly, x):
    return x.parent()['x'](poly)(x=x)


def build_ext(k, ds):
    R = Zmod(2^k)
    F = GF(2)
    for i, d in enumerate(ds):
        PR = R[f"a{i}"]
        a = PR.gen()
        PF = F[f"b{i}"]
        b = PF.gen()
        while True:
            m = b^d + rand(PF, d)
            if m.is_irreducible():
                print(m)
                F = PF.quo(m)
                nm = fromlist(PR, tolist(m), d=d+1)
                R = PR.quo(nm)
                break
    return R


def chal(k, ds):
    R1 = build_ext(k, ds)
    R2 = build_ext(k, [prod(ds)])
    poly = [secrets.randbelow(3) - 1 for _ in range(1024)]
    pt1 = rand(R1)
    print(",".join(map(str, tolist(pt1))))
    pt2 = fromlist(R2, (int(x) for x in input("> ").split(",")))
    print(",".join(map(str, tolist(evalp(poly, pt2)))))
    K.extend(tolist(evalp(poly, pt1)))


if __name__ == "__main__":
    K = []
    chal( 2, [2, 3]   )
    chal( 8, [2, 3]   )
    chal( 8, [2, 3, 5])
    chal(32, [3, 4, 5])
    chal(64, [4, 3, 5])
    key = hashlib.sha256("||".join(map(str, K)).encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC)
    print(cipher.iv.hex(), cipher.encrypt(pad(flag.encode(), AES.block_size)).hex())
