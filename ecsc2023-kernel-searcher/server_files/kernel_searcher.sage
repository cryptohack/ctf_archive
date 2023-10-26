#! /usr/local/bin/sage

def generate_point(E):
    """
    Generate points on a curve E with x-coordinate
    i + x for x in Fp and i is the generator of Fp^2
    such that i^2 = -1.
    """
    F = E.base_ring()
    one = F.one()
    x = F.gen() + one

    for _ in range(1000):
        if E.is_x_coord(x):
            yield E.lift_x(x)
        x += one

    raise ValueError(
        "Generated 1000 points, something is probably going wrong somewhere."
    )


def generate_point_order_D(E, D):
    """
    Compute a point of order D on E
    """
    p = E.base().characteristic()
    k = (p + 1) // D

    Ps = generate_point(E)
    for G in Ps:
        P = k*G

        # Check that P has order exactly D
        if P.order() == D:
            yield P

    raise ValueError(f"Never found a point P of order D.")

def canonical_torsion_basis(E, D):
    """
    Generate basis of E(Fp^2)[D] of supersingular curve
    """
    Ps = generate_point_order_D(E, D)
    P = Ps.__next__()
    for Q in Ps:
        assert P.order() == D
        assert Q.order() == D

        ePQ = P.weil_pairing(Q, D)
        if ePQ.multiplicative_order() == D:
            return P, Q

# ======================= #
#  Challenge Starts Here  #
# ======================= #

import json
from Crypto.Util.number import bytes_to_long

proof.all(False)

A, B = 2**216, 3**137
p = A * B - 1

F.<i> = GF(p^2, modulus=[1,0,1])
E = EllipticCurve(F, [0, 6, 0, 1, 0])

# Torsion Basis for E[A]
P, Q = canonical_torsion_basis(E, A)

import os
flag = os.environ.get("FLAG", "ECSC{fake_flag_for_testing}").strip().encode()
ker = P + bytes_to_long(flag) * Q
challenge_isogeny = E.isogeny(
    ker, algorithm="factored", model="montgomery"
)

def accept_point(data):
    data = json.loads(data)
    try:
        x0 = int(data["x0"], 16)
        x1 = int(data["x1"], 16)
        x = F([x0, x1])
    except Exception as e:
        print(e)
        return {"error": "Invalid Fp2 value"}
    
    if not E.is_x_coord(x):
        return {"error": "Invalid Point"}

    P = E.lift_x(x)
    imP = challenge_isogeny(P)
    return json.dumps({"x0": hex(imP[0][0]), "x1": hex(imP[0][1])})

def main():
    print(f"Welcome to my isogeny factory!")
    print(f"My isogeny is so secret, I'll let you evaluate any point you like!")
    while True:
        data = input("Send the point you wish to evaluate: ")
        output = accept_point(data)
        print(output)

if __name__ == "__main__":
    main()




