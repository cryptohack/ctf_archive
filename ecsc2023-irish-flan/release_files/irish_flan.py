import hashlib
import secrets
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad


def Z(M):
    class R:
        def __init__(self, r):
            self.r = r % M

        def __add__(self, other):
            return R(self.r + other.r)

        def __sub__(self, other):
            return R(self.r - other.r)

        def __neg__(self):
            return R(-self.r)

        def __mul__(self, other):
            if isinstance(other, int):
                return R(self.r * other)
            return R(self.r * other.r)

        def __pow__(self, other):
            return R(pow(self.r, other, M))

        def __truediv__(self, other):
            return self * other**-1

        def __repr__(self):
            return f"Z({repr(M)})({repr(self.r)})"

        def __str__(self):
            return f"{self.r} (mod {M})"
    return R


class Q:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __add__(self, other):
        return Q(self.a + other.a, self.b + other.b,
                 self.c + other.c, self.d + other.d)

    def __sub__(self, other):
        return Q(self.a - other.a, self.b - other.b,
                 self.c - other.c, self.d - other.d)

    def __mul__(self, o):
        if isinstance(o, (int, type(self.a))):
            return Q(self.a * o, self.b * o,
                     self.c * o, self.d * o)
        return Q(self.a * o.a - self.b * o.b - self.c * o.c - self.d * o.d,
                 self.a * o.b + self.b * o.a + self.c * o.d - self.d * o.c,
                 self.a * o.c - self.b * o.d + self.c * o.a + self.d * o.b,
                 self.a * o.d + self.b * o.c - self.c * o.b + self.d * o.a
                 )

    def __pow__(self, other):
        if other < 0:
            return self.invert()**-other
        res = Q(*map(type(self.a), [1, 0, 0, 0]))
        c = self
        while other:
            if other & 1:
                res = res * c
            other >>= 1
            c = c * self
        return res

    def invert(self):
        d = (self.a**2 + self.b**2 + self.c**2 + self.d**2)
        return Q(self.a/d, -self.b/d, -self.c/d, -self.d/d)

    def __repr__(self):
        return "Q({},{},{},{})".format(*map(repr,
                                       [self.a, self.b, self.c, self.d]))

    def __str__(self):
        return "({})".format(",".join(
                             map(str, [self.a, self.b, self.c, self.d])))


class Dessert:
    def __init__(self):
        self.n = getPrime(1024) * getPrime(1024)
        self.R = Z(self.n)
        r = secrets.randbelow(self.n**8)
        self.χ = Q(*[self.R(secrets.randbelow(self.n)) for _ in "abcd"])
        self.α = Q(*[self.R(secrets.randbelow(self.n)) for _ in "abcd"])
        self.β = self.χ**-1 * self.α**-1 * self.χ
        self.γ = self.χ**r

    @property
    def pub(self):
        return (self.n,
                self.α,
                self.β,
                self.γ)

    def encrypt(self, m):
        k = Q(*[self.R(secrets.randbelow(self.n)) for _ in "abcd"])
        K = hashlib.sha256(str(k).encode()).digest()
        c = AES.new(K, AES.MODE_CBC, iv=b"\0" * 16).encrypt(pad(m, 16))
        s = secrets.randbelow(self.n**8)
        δ = self.γ**s
        ε = δ**-1 * self.α * δ
        κ = δ**-1 * self.β * δ
        μ = κ * k * κ
        return (c, μ, ε)


if __name__ == "__main__":
    flan = Dessert()
    print("Public key:", ",".join(map(str, flan.pub)))
    with open("flag.txt") as f:
        print("Encryption:", ",".join(
              map(str, flan.encrypt(f.read().strip().encode()))))
