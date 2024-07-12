import random
from Crypto.Util.number import bytes_to_long
from params import P, q, g
from hashlib import sha512
import json
import os

FLAG = os.environ["FLAG"].encode()

# kinda a random oracle
def Totally_a_random_oracle(a0,a1,e,e0,e1,z0,z1):
    ROstep = sha512(b'my')
    ROstep.update(str(a0).encode())
    ROstep.update(b'very')
    ROstep.update(str(a1).encode())
    ROstep.update(b'cool')
    ROstep.update(str(e).encode())
    ROstep.update(b'random')
    ROstep.update(str(e0).encode())
    ROstep.update(b'oracle')
    ROstep.update(str(e1).encode())
    ROstep.update(b'for')
    ROstep.update(str(z0).encode())
    ROstep.update(b'fischlin')
    ROstep.update(str(z1).encode())
    res = bytes_to_long(ROstep.digest())
    return res

def fischlin_proof(w0,w1,y0,y1,b):
    if b:
        w_sim, w_b, y_sim, y_b = w0, w1, y0, y1
    else:
        w_sim, w_b, y_sim, y_b = w1, w0, y1, y0

    r_b = random.randint(0,q)
    a_b = pow(g,r_b,P)
    # Simulate transcript 1
    e_sim = random.randint(0,2**511)
    z_sim = pow(g,random.randint(0,q), P)
    a_sim = (pow(pow(y_sim,e_sim,P),-1,P) *pow(g,z_sim,P)) % P
    
    # Normally you would sample for some `t` rounds, with `rho` parallel iterations
    # We simplify slightly for the purposes of this challenge. 
    # we just use `t` = 2**10, and `B` = 6, (and for this challenge we ignore parallel repititions/what happens if B is never hit)
    t = 2**10
    B = 6
    for e in range(t):
        # complete real transcript
        e_b = e^e_sim
        z_b = (r_b + e_b*w_b) % q

        # fix blinding
        if b:
            a0, a1, e0, e1, z0, z1 = a_sim, a_b, e_sim, e_b, z_sim, z_b
        else:
            a1, a0, e1, e0, z1, z0 = a_sim, a_b, e_sim, e_b, z_sim, z_b

        # if result of "random oracle" is small enough, we go with this transcript \o/
        res = Totally_a_random_oracle(a0,a1,e,e0,e1,z0,z1)
        if res < 2**(512-B):
            break

    proof = {}
    proof["a0"] = a0
    proof["a1"] = a1
    proof["e"] = e
    proof["e0"] = e0
    proof["e1"] = e1
    proof["z0"] = z0
    proof["z1"] = z1

    return proof


def gen_round():
    w0 = random.randint(0,q)
    y0 = pow(g,w0,P)
    w1 = random.randint(0,q)
    y1 = pow(g,w1,P)
    assert (y0%P) >= 1 and (y1%P) >= 1
    assert pow(y0, q, P) == 1 and pow(y1, q, P) == 1
    return w0, w1, y0, y1

attempts = 2**4

for round in range(64):
    print(f'round: {round}')
    print(f'I will prove knowledge of one of these dlogs, using either w0 or w1')
    
    for i in range(attempts):
        w0,w1,y0,y1 = gen_round()

        print(f'y0 = {y0}')
        print(f'y1 = {y1}')
        leak_witness = int(input("which witness do you want to see?"))
        if leak_witness:
            print(f'w1 = {w1}')
        else:
            print(f'w0 = {w0}')

        # choose which witness will be used for the proof
        b = int(random.randint(0,1))

        # Gives transcript (a0,a1) e (e0,e1,z0,z1) made using witness `b` where:
        # (a0,e0,z0) and (a1,e1,z1) are satisfying transcripts
        # e0 xor e1 = e 
        # RO(a0,a1,e,e0,e1,z0,z1) has `B` leading zeroes
        proof = fischlin_proof(w0,w1,y0,y1,b)

        print(f'here is your fishlin transcript')
        print(json.dumps(proof))

        trying = input("do you think you can guess my witness? (y,n)")
        if trying.lower().startswith("n"):
            continue
        else:
            break

    b_guess = int(input("which witness did the prover use?"))
    if b == b_guess:
        print("wow you distinguished my witness!")
        print(f'do it {64-round} times more for flag!')
    else:
        print("you didn't guess the right witness")
        print("skill issue + L + ratio + not able to distinguish the witness in a fischlin transform")
        exit()

print("well done, you distinguished all the witnesses!")
print(FLAG)
