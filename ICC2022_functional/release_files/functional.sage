import numpy as np
from secret_params import (COEFFS,
                            ITERS # ITERS = secrets.randrange(13**37)
                            )
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

F = GF(2^142 - 111)

def f(n):
    if n < len(COEFFS):
        return F(int(10000*np.sin(n)))
    return COEFFS.dot(list(map(f, n - 1 - np.arange(len(COEFFS)))))

def g(n):
    if n < 6:
        return F(int(10000*np.sin(len(COEFFS) + n)))
    return np.array([F(int(10000*np.log10(2 + i))) for i in range(6)]).dot([g(n - 6), h(n - 2), i(n - 3), g(n - 3), h(n - 4), i(n)]) + 2*n**3 + 42

def h(n):
    if n < 3:
        return F(int(10000*np.sin(len(COEFFS) + 6 + n)))
    return np.array([F(int(10000*np.log10(1337 + i))) for i in range(4)]).dot([h(n - 3), i(n - 1), g(n - 2), h(n - 1)]) + n

def i(n):
    if n < 3:
        return F(int(10000*np.sin(len(COEFFS) + 9 + n)))
    return np.array([F(int(10000*np.log10(31337 + i))) for i in range(5)]).dot([i(n - 2), g(n - 3), h(n - 3), h(n - 1), i(n - 1)]) + 1

def j(n):
    if n < 10^4:
        return F(sum(S3[d] for d in ZZ(n).digits(1337)))
    return np.array([F(int(10000*np.log(31337 + i))) for i in range(100)]).dot(list(map(j, n - 10^4 + 100 - np.arange(100))))

if __name__ == "__main__":
    print("Stage 1:")
    print("========")
    print([f(ITERS + k) for k in range(500)])

    print("Stage 2:")
    print("========")
    S3 = [i(ITERS + k) for k in range(1337)]

    print("Stage 3:")
    print("========")
    key = hashlib.sha256(str(j(ITERS)).encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    with open("flag.txt", "rb") as f:
        print(cipher.encrypt(pad(f.read().strip(), 16)).hex())
