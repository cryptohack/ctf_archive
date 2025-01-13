#!/usr/bin/env python3

from Crypto.PublicKey.ECC import EccPoint
from Crypto.Random import random
import hashlib
import json
import os

flag = os.getenv('FLAG', 'ECSC{redacted}')

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = EccPoint(Gx, Gy)
H = None


class Ciphertext:
    def __init__(self, value):
        self.R = value[0]
        self.S = value[1]

    @classmethod
    def from_pt(cls, m):
        r = random.randint(0, q-1)
        R = r*G
        S = r*H + m*G
        return cls([R, S])

    def __add__(self, other):
        if isinstance(other, int):
            return self + Ciphertext.from_pt(other)
        rand = Ciphertext.from_pt(0)
        return Ciphertext([self.R+other.R+rand.R, self.S+other.S+rand.S])

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError
        rand = Ciphertext.from_pt(0)
        return Ciphertext([rand.R + other*self.R, rand.S + other*self.S])
    
    def __neg__(self):
        return Ciphertext([-self.R, -self.S])

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        if isinstance(other, int):
            return Ciphertext.from_pt(other) - self
        

def round():
    data = json.loads(input("Send your encrypted choice bit: "))
    C = Ciphertext([EccPoint(data["Rx"], data["Ry"]), EccPoint(data["Sx"], data["Sy"])])
    m0 = random.randint(0, 9)
    m1 = random.randint(0, 9)
    res = m0 * (1-C) + m1 * C
    print(json.dumps({"Rx": int(res.R.x), "Ry": int(res.R.y), "Sx": int(res.S.x), "Sy": int(res.S.y)}))
    data = json.loads(input("Send the recovered messages: "))
    return m0 == data["m0"] and m1 == data["m1"]

def get_pk():
    global H
    data = json.loads(input("Send your public key: "))
    H = EccPoint(data["Hx"], data["Hy"])
    assert H != G


def main():
    print("Welcome to my new guessing game! Are you ready?")
    get_pk()

    for _ in range(128):
        assert round()

    print(flag)


if __name__ == "__main__":
    main()