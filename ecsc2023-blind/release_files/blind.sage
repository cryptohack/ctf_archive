import secrets, hashlib, bcrypt, operator, random
from Crypto.Cipher import AES

def get_curve():
    # https://neuromancer.sk/std/other/Ed448
    p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    K = GF(p)
    a = K(0x01)
    d = K(0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffffffffffffffffffffffffffffffffffffffff6756)
    E = EllipticCurve(K, (K(-1/48) * (a^2 + 14*a*d + d^2),K(1/864) * (a + d) * (-a^2 + 34*a*d - d^2)))
    def to_weierstrass(x, y):
        return ((5*a + a*y - 5*d*y - d)/(12 - 12*y), (a + a*y - d*y -d)/(4*x - 4*x*y))
    def to_twistededwards(u, v):
        y = (5*a - 12*u - d)/(-12*u - a + 5*d)
        x = (a + a*y - d*y -d)/(4*v - 4*v*y)
        return (x, y)
    G = E(*to_weierstrass(K(0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa955555555555555555555555555555555555555555555555555555555), K(0xae05e9634ad7048db359d6205086c2b0036ed7a035884dd7b7e36d728ad8c4b80d6565833a2a3098bbbcb2bed1cda06bdaeafbcdea9386ed)))
    E.set_order(0x3fffffffffffffffffffffffffffffffffffffffffffffffffffffff7cca23e9c44edb49aed63690216cc2728dc58f552378c292ab5844f3 * 0x04)
    # This curve is a Weierstrass curve (SAGE does not support TwistedEdwards curves) birationally equivalent to the intended curve.
# You can use the to_weierstrass and to_twistededwards functions to convert the points.
    return E, G, to_weierstrass, to_twistededwards

q = 2^448 - 2^224 - 1
E, G, to_weierstrass, to_twistededwards = get_curve()
p = int(G.order())
k = 8*((len(bin(p)) - 2 + 7) // 8)
k2 = 128
k1 = 8*((7 + len(bin(q)) - 2)//8) - k2

def Hash(x, nin, n, div):
    assert nin % 8 == n % 8 == 0
    nin //= 8
    n //= 8
    assert len(x) == nin
    r = b""
    i = 0
    while len(r) < n:
        r += hashlib.sha256(x + b"||" + div + int(i).to_bytes(8, "big")).digest()
        i += 1
    return r[:n]

F1 = lambda x: Hash(x, k2, k1, b"1")
F2 = lambda x: Hash(x, k1, k2, b"2")
H = lambda x: Hash(x, k1+k2, k, b"H")

def xor(a, b):
    assert len(a) == len(b)
    return bytes(map(operator.xor, a, b))

def keygen():
    x = secrets.randbelow(p)
    Y = -x * G
    return (Y, x)

def sign(m, x):
    m1 = F1(m) + xor(F2(F1(m)), m)
    ω = secrets.randbelow(p)
    r = xor(int((ω * G)[0]).to_bytes((k1 + k2)//8, "big"), m1)
    c = int.from_bytes(H(r), "big")
    z = (ω + c * x) % p
    return (r.hex(), z)

def encrypt_flag():
    k = secrets.token_bytes(k2//8)
    key = bcrypt.kdf(k, b"ICC_CHALLENGE", 16, 31337)
    cipher = AES.new(key, AES.MODE_CTR, nonce=b"")
    with open("flag.txt", "rb") as f:
        flag = f.read().strip()
    return k, cipher.encrypt(flag)

def main():
    Y, x = keygen()
    _k, ct = encrypt_flag()

    print(f"Y = {to_twistededwards(*Y.xy())}")
    print(f"ct = {ct.hex()}")
    sigs = []
    sigs.append(sign(_k, x))
    for _ in range(10000 - 1):
        sigs.append((secrets.token_bytes((k1 + k2)//8).hex(), secrets.randbelow(p)))
    random.seed(secrets.token_bytes(16))
    random.shuffle(sigs)
    print(sigs)

if __name__ == "__main__":
    main()
