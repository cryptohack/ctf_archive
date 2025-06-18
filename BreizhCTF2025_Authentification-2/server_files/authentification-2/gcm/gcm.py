"""

Title       : AES-GCM
Author      : Bill (intern)
Description : Implementation — algorithm by algorithm — of this NIST publication [1].
              I had to speedrun due to the short duration of my internship.
              I'm not sure that everything is correct...

References :
    - [1] : https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf

"""

from .utils import xor, bytes_to_bits, bits_to_bytes
from Crypto.Cipher import AES
from math import ceil

BLOCK_LEN = 16
CTR_LEN   = 4
IV_LEN    = 12

class GCM:
    def __init__(self, key, iv):
        assert len(key) == BLOCK_LEN
        assert len(iv) == IV_LEN

        self.cipher = AES.new(key, AES.MODE_ECB)
        self.key = key
        self.iv  = iv
        self.H = self.cipher.encrypt(b"\x00"*BLOCK_LEN)

    # 6.2 Incrementing function
    def inc(self, X: bytes, s=CTR_LEN):
        assert len(X) == BLOCK_LEN
        ctr = int.from_bytes(X[-s:], "big") + 1
        return X[:-s] + ctr.to_bytes(s, byteorder="big")

    # Algorithm 1: X*Y
    def mul(self, X: bytes, Y: bytes):
        assert len(X) == len(Y) == BLOCK_LEN

        R = bytes_to_bits(b"\xe1" + b"\x00"*(BLOCK_LEN-1))
        X = bytes_to_bits(X)
        V = bytes_to_bits(Y)
        Z = [0x00 for _ in range(BLOCK_LEN*8)]

        for i in range(BLOCK_LEN*8):
            if X[i] == 0:
                Z = Z
            else:
                Z = [z^v for z,v in zip(Z,V)]

            if V[-1] == 0:
                V = [0] + V[:-1]
            else:
                V = [0] + V[:-1]
                V = [v^r for v,r in zip(V, R)]
            
        return bits_to_bytes(Z)

    # Algorithm 2: GHASH
    def ghash(self, X: bytes, H: bytes):
        assert len(X) % BLOCK_LEN == 0
        assert len(H) == BLOCK_LEN

        Y  = b"\x00"*BLOCK_LEN
        Xs = [X[i:i+BLOCK_LEN] for i in range(0, len(X), BLOCK_LEN)]
        m  = len(X)//BLOCK_LEN

        for i in range(m):
            Y = self.mul(xor(Y, Xs[i]), H)

        return Y

    # Algorithm 3: GCTR
    def gctr(self, ICB: bytes, X: bytes):
        assert len(ICB) == BLOCK_LEN

        if X == b"":
            return b""

        Xs = [X[i:i+BLOCK_LEN] for i in range(0, len(X), BLOCK_LEN)]
        n = ceil(len(X) / BLOCK_LEN)
        CB = ICB[:]
        Y = b""

        for i in range(0, n-1):
            Y += xor(Xs[i], self.cipher.encrypt(CB))
            CB = self.inc(CB)

        Y += xor(Xs[-1], self.cipher.encrypt(CB)[:len(Xs[-1])])
        return Y

    def build_tag(self, C, A, J):
        u = BLOCK_LEN * ceil(len(C)/BLOCK_LEN) - len(C)
        v = BLOCK_LEN * ceil(len(A)/BLOCK_LEN) - len(A)

        buf =  b""
        buf += A + b"\x00"*v + C + b"\x00"*u 
        buf += (len(A)*8).to_bytes(8, "big") 
        buf += (len(C)*8).to_bytes(8, "big")

        S = self.ghash(buf, self.H)

        return self.gctr(J, S)

    # Algorithm 4: GCM-AE_K
    def encrypt(self, P, A=b""):
        J = self.iv + b"\x00"*(CTR_LEN-1) + b"\x01"
        C = self.gctr(J, P)
        T = self.build_tag(C, A, J)

        return C, T

    # Algorithm 5: GCM-AD_K
    def decrypt(self, C, T, A=b""):
        assert len(T) == BLOCK_LEN
        J = self.iv + b"\x00"*(CTR_LEN-1) + b"\x01"
        P = self.gctr(J, C)

        TT = self.build_tag(C, A, J)
        
        if TT != T:
            return (P, False)

        return (P, True)

