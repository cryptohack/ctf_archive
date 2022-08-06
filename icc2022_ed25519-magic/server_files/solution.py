from pwn import *
import pure25519
import pure25519.basic as basic

def new_level():
    p.recvline()
    p.recvline()
    p.recvline()

def signature_add_l(signature):
    assert len(signature) == 64
    r, s = signature[:32], signature[32:]

    new_s = basic.bytes_to_scalar(s) + basic.L*15
    import math
    print(math.log(new_s, 2))
    # print(math.log(basic.L * 2, 2))
    new_s = binascii.unhexlify("%064x" % new_s)[::-1]

    return base64.b64encode(r + new_s)

level = "info"
level = "debug"
# p = process(['python3', 'chal.py'], level = level)
p = remote("localhost", 13371, level = level)

# level1
new_level()
p.recvline()
sig = p.recvline()
p.recvline()
sig_data = base64.b64decode(sig)
new_sig = signature_add_l(sig_data)
p.sendline(new_sig)

# level2
new_level()
p.recvline()
vk = "AQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
p.sendline(vk)
p.recvline()
sig = "Sb1LmJq8FptB6GSTbi6IjYARGJM09wdk1MNkSHI59I1S/ItySz94QLLGjsbxupFy168PGqHqas3Fmd2PJk+yAw=="
p.sendline(sig)

print(p.recvline())
