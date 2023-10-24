import secrets


def drbg():
    # wuch wow, very deterministic
    return secrets.randbelow(2)


def sample_noise(n):
    e = 0
    for _ in range(n):
        e |= drbg()
        e <<= 1
    return e


def sample_key():
    # LWE estimator told me I'd have more bits of security than bits in my key...
    return secrets.token_bytes(16)


def get_flag():
    with open("flag.txt") as f:
        bs = f.read().strip().encode()
    return [(b >> i) & 1 for b in bs for i in range(8)]


def dot(a, s):
    return sum(x * y for x, y in zip(a, s))


def real(s):
    a = secrets.token_bytes(len(s))
    e = sample_noise(7) - 64
    return a, (dot(a, s) + e) % 256


def fake(s):
    a = secrets.token_bytes(len(s))
    return a, secrets.randbelow(256)


if __name__ == "__main__":
    s = sample_key()
    for b in get_flag():
        print([[real, fake][b](s) for _ in range(6)])
