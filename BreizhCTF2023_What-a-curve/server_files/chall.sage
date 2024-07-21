import os
import struct
from random import SystemRandom

flag = os.environ.get("FLAG").encode()

p = 17585255163044402023

R.<x> = GF(p)[];
f = sum([SystemRandom().randrange(0,p)*x^i for i in range(16)])
C = HyperellipticCurve(f, 0)
J = C.jacobian()

class RNG(object):

    def __init__(self,seed=0):
        if seed == 0:
            self.mul = SystemRandom().randrange(2024,p)
        else:
            self.mul = seed
        self.point = None
        while self.point is None:
            x = SystemRandom().randrange(0,p)
            if len(f(x).sqrt(0,1)) == 0:
                continue
            self.point = J(C(x, min(f(x).sqrt(0,1))))
        self.out = []

    def update(self):
        self.point = self.mul*self.point
        return self.point

    def __call__(self):
        if not self.out:
            u,v = self.update()
            rs = [u[i] for i in range(7)] + [v[i] for i in range(7)]
            assert 0 not in rs and 1 not in rs
            self.out = struct.pack('<'+'Q'*len(rs), *rs)
        r, self.out = self.out[0], self.out[1:]
        return r

    def __iter__(self): return self
    def __next__(self): return self()

print(bytes(k^^m for k,m in zip(RNG(2023), flag+b" This is your final boss, enjoy it while you still can:)")).hex())

while True:
    try:
        msg = bytes.fromhex(input("Enter your message : \n"))
        print(bytes(k^^m for k,m in zip(RNG(), msg)).hex())
    except:
        break
