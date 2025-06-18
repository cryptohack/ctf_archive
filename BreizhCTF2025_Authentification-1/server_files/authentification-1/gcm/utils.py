def xor(X, Y):
    assert len(X) == len(Y)
    return bytes([x^y for x,y in zip(X, Y)])

def bytes_to_bits(X: bytes):
    res = []

    for b in X:
        for bb in bin(b)[2:].zfill(8):
            res.append(int(bb))

    return res

def bits_to_bytes(X):
    X = [str(x) for x in X]
    res = []

    for b in range(0, len(X), 8):
        res.append(int("".join(X[b:b+8]), 2))

    return bytes(res)

