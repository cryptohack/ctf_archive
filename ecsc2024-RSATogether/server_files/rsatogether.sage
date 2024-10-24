#!/usr/bin/env sage

from Crypto.Util.number import getPrime, bytes_to_long
import random
import os

random = random.SystemRandom()

flag = os.getenv("FLAG", "ECSC{testflag}")

def gen_key(n_bits):
    p = getPrime(n_bits//2)
    q = getPrime(n_bits//2)
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, phi)

    return phi, d, n, e

def eval_poly(poly, x, n):
    return sum(pow(x, i, n) * poly[i] for i in range(len(poly))) % n

def create_shares(phi, poly):
    n_shares = int(input("With how many friends you want to share the private key? "))

    if n_shares < 1:
        print("Don't be mean, sharing is caring!")
        exit()
    elif n_shares > 101:
        print("Come on, you don't have that many friends...")
        exit()

    n_shares += 1 # you also get one part of the key, don't worry
    poly = poly[:n_shares]
    ys = [eval_poly(poly, i, phi) for i in range(1, n_shares+1)]
    M = matrix(ZZ, [[x**i for i in range(n_shares)] for x in range(1, n_shares+1)])
    coeffs = M.solve_left(vector(ZZ, [1] + [0]*(n_shares - 1)))

    shares = [(c*y) % phi for c,y in zip(coeffs, ys)]
    yours = shares.pop(n_shares - 2)
    print(f"Here is your part: {yours}")

    return shares


def comput_partial_decryption(c, shares, n):
    return [pow(c, s, n) for s in shares]


n_bits = 2048
phi, d, n, e = gen_key(n_bits)
print(f"{n = }")
print(f"{e = }")

poly = [d] + [random.getrandbits(n_bits) for _ in range(99)]
shares = create_shares(phi, poly)

while True:
    choice = int(input("""
Select:
1) Decrypt something
2) Reshare
3) That's enough
> """))
    if choice == 1:
        c = int(input("Ciphertext: "))
        partial_dec = comput_partial_decryption(c, shares, n)
        print("Here are the partial decryptions of your friends!")
        for pt in partial_dec:
            print(pt)
    elif choice == 2:
        shares = create_shares(phi, poly)
    elif choice == 3:
        break

pad_flag = os.urandom((n_bits - 8)//8 - len(flag)) + flag.encode()
print(f"Bye bye, take this with you!\n{pow(bytes_to_long(pad_flag), e , n)}")
