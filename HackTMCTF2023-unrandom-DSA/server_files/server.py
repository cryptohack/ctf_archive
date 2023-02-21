import os
import random
import signal

signal.alarm(600)
flag = os.environ.get("FLAG", "FAKEFLAG{THIS_IS_FAKE}")

try:
    q = int(input("q = "))
    p = int(input("p = "))
    g = int(input("g = "))
    x = random.SystemRandom().randint(1, q - 1)
    y = pow(g, x, p)
    seed = int(input("What's your favorite number (hex): "), 16)

    # urandom is unrandom
    os.urandom = random.randbytes

    from Crypto.Hash import SHA256
    from Crypto.PublicKey import DSA
    from Crypto.Signature import DSS

    random.seed(seed)

    dsa = DSA.construct((y, g, p, q, x))
    dss = DSS.new(dsa, "fips-186-3")
    print(f"{y = }")
    sign = bytes.fromhex(input("sign = "))
    # if verify is failed, it raises ValueError
    dss.verify(SHA256.new(b"sign me!"), sign)
    print(flag)
except Exception as e:
    print(e)
