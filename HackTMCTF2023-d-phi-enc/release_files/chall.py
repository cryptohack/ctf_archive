import os

from Crypto.Util.number import bytes_to_long, getStrongPrime

flag = os.environ.get("FLAG", "FAKEFLAG{" + "A" * 245 + "}").encode()
assert len(flag) == 255
e = 3
p = getStrongPrime(1024, e=e)
q = getStrongPrime(1024, e=e)
n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
enc_d = pow(d, e, n)
enc_phi = pow(phi, e, n)
enc_flag = pow(bytes_to_long(flag), e, n)
print(f"{n = }")
print(f"{enc_d = }")
print(f"{enc_phi = }")
print(f"{enc_flag = }")
