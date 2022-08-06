from Crypto.Util.number import bytes_to_long, getPrime

def gen_keys(n_bits, p_bits, d_bits):
    q_bits = n_bits - p_bits
    p, q = getPrime(p_bits), getPrime(q_bits)
    N, phi = p*q, (p-1)*(q-1)
    while True:
        d = getPrime(d_bits)
        if d > N**0.292:
            break
    e = pow(d,-1,phi)
    return (N, e), (N, d)

def encrypt_flag(plaintext, pub):
    N, e = pub
    m = bytes_to_long(plaintext)
    return pow(m, e, N)

if __name__ == '__main__':
    with open("flag.txt", "rb") as f:
        flag = f.read().strip()

    n_bits = 1024
    p_bits = 256
    d_bits = 300
    pub, priv = gen_keys(n_bits, p_bits, d_bits)
    c = encrypt_flag(flag, pub)

    print(f"N = {hex(pub[0])}")
    print(f"e = {hex(pub[1])}")
    print(f"c = {hex(c)}")