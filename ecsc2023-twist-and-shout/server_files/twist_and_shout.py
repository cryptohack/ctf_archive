"""
Define the elliptic curve

E: y^2 = x^3 + a*x + b

With order

n = 340282366920938463465004184633952524077
  = 2^128 - 1629577202184312621
"""
q = 2**128 - 159
a = 1
b = 1494


# Curve addition law using only x-coordinates, coded from
# https://www.hyperelliptic.org/EFD/g1p/data/shortw/xz/ladder/ladd-2002-it
def xDBLADD(P, Q, PQ):
    (X1, Z1), (X2, Z2), (X3, Z3) = PQ, P, Q
    X4 = (X2**2 - a * Z2**2) ** 2 - 8 * b * X2 * Z2**3
    Z4 = 4 * (X2 * Z2 * (X2**2 + a * Z2**2) + b * Z2**4)
    X5 = Z1 * ((X2 * X3 - a * Z2 * Z3) ** 2 - 4 * b * Z2 * Z3 * (X2 * Z3 + X3 * Z2))
    Z5 = X1 * (X2 * Z3 - X3 * Z2) ** 2
    X4, Z4, X5, Z5 = (c % q for c in (X4, Z4, X5, Z5))
    return (X4, Z4), (X5, Z5)


# Montgomery Ladder for scalar multiplication
def xMUL(P, k):
    Q, R = (1, 0), P
    for i in reversed(range(k.bit_length() + 1)):
        if k >> i & 1:
            R, Q = Q, R
        Q, R = xDBLADD(Q, R, P)
        if k >> i & 1:
            R, Q = Q, R
    return Q


def gen_secret(secret):
    d = secret.lstrip("ECSC{").rstrip("}")
    return int.from_bytes(d.encode(), "big")


def shout(x, d):
    P = (x, 1)
    Q = xMUL(P, d)
    return Q[0] * pow(Q[1], -1, q) % q


def challenge():
    """
    My curve has prime order, so I'll let you
    send as many points as you like! You'll
    never recover my secret before your flight home!!
    """
    import os
    flag = os.environ.get("FLAG", "ECSC{fake_flag_for_testing}").strip()
    d = gen_secret(flag)

    while True:
        x = int(input("x-coordinate: "))
        print(shout(x, d))


if __name__ == "__main__":
    challenge()
