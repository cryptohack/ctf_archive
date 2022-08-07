from collections import namedtuple
from Crypto.Util.number import getPrime
import random
 
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
 
 
def generate_key_pair(nbits):
    while True:
        p = getPrime((nbits + 3) // 4)
        q = getPrime((nbits + 3) // 4)
        n = (p ** 2) * (q ** 2)
        if n.bit_length() == nbits:
            return (p, q), n
 
 
def pad(data, length):
    assert len(data) < length
    pad_length = length - len(data) - 1
    pad_data = bytes(random.choices(range(1, 256), k=pad_length))
    sep = b'\x00'
    return pad_data + sep + data
 
 
def unpad(data):
    assert b"\x00" in data, "incorrect padding"
    return data.split(b"\x00", 1)[1]
 
 
def encrypt(public_key, plaintext):
    n = public_key
    plaintext = pad(plaintext, 2 * ((n.bit_length() - 1) // 8))
    m = Complex(
        int.from_bytes(plaintext[:len(plaintext) // 2], "big"),
        int.from_bytes(plaintext[len(plaintext) // 2:], "big")
    )
    c = complex_pow(m, 65537, n)
    return (c.re.to_bytes((n.bit_length() + 7) // 8, "big")
            + c.im.to_bytes((n.bit_length() + 7) // 8, "big"))
 
 
def decrypt(private_key, ciphertext):
    # TODO
    raise Exception("unimplemented")
 
 
def main():
    private_key, public_key = generate_key_pair(2021)
    from secret import flag
 
    print("private_key =", private_key)
    print("public_key =", public_key)
    print("ciphertext =", encrypt(public_key, flag))
 
 
if __name__ == '__main__':
    main()