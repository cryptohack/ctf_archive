from collections import namedtuple
from Crypto.Util.number import getPrime, isPrime, getRandomRange
 
Complex = namedtuple("Complex", ["re", "im"])
 
 
def complex_mult(c1, c2, modulus):
    return Complex(
        (c1.re * c2.re - c1.im * c2.im) % modulus,  # real part
        (c1.re * c2.im + c1.im * c2.re) % modulus,  # image part
    )
 
 
def complex_pow(c, exp, modulus):
    result = Complex(1, 0)
    while exp > 0:
        if exp & 1:
            result = complex_mult(result, c, modulus)
        c = complex_mult(c, c, modulus)
        exp >>= 1
    return result
 
 
class ComplexDiffieHellman:
    @staticmethod
    def generate_params(prime_length):
        # Warning: this may take some time :)
        while True:
            p = getPrime(prime_length)
            if p % 4 == 3:
                if p % 3 == 2:
                    q = (p - 1) // 2
                    r = (p + 1) // 12
                    if isPrime(q) and isPrime(r):
                        break
                else:
                    q = (p - 1) // 6
                    r = (p + 1) // 4
                    if isPrime(q) and isPrime(r):
                        break
        n = p ** 2
        order = p * q * r
        while True:
            re = getRandomRange(1, n)
            im = getRandomRange(1, n)
            g = complex_pow(Complex(re, im), 24, n)
            if (
                    complex_pow(g, order, n) == Complex(1, 0)
                    and complex_pow(g, order // p, n) != Complex(1, 0)
                    and complex_pow(g, order // q, n) != Complex(1, 0)
                    and complex_pow(g, order // r, n) != Complex(1, 0)
            ):
                return g, order, n
 
    def __init__(self, params=None, prime_length=128, debug=False):
        if not debug:
            raise Exception("security unevaluated")
        if params is None:
            params = ComplexDiffieHellman.generate_params(prime_length)
        self.g, self.order, self.n = params
 
    def get_public_key(self, private_key):
        return complex_pow(self.g, private_key, self.n)
 
    def get_shared_secret(self, private_key, other_public_key):
        return complex_pow(other_public_key, private_key, self.n)
 
 
def main():
    from os import urandom
    private_key = urandom(32)
    k = int.from_bytes(private_key, "big")
 
    cdh = ComplexDiffieHellman(debug=True)
    print("g =", cdh.g)
    print("order =", cdh.order)
    print("n =", cdh.n)
    print("public_key =", cdh.get_public_key(k))
 
    # Solve the discrete logarithm problem if you want the flag :)
    from secret import flag
    from Crypto.Cipher import AES
    if len(flag) % 16 != 0:
        flag += b"\x00" * (16 - len(flag) % 16)
    print("encrypted_flag = ",
          AES.new(private_key, AES.MODE_ECB).encrypt(flag))
 
 
if __name__ == "__main__":
    main()