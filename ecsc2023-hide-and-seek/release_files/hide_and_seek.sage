from Crypto.Util.number import bytes_to_long
FLAG = bytes_to_long(open("flag.txt", "rb").read().strip()[len("ECSC{"):-1])

proof.arithmetic(False)
p = 1789850433742566803999659961102071018708588095996784752439608585988988036381340404632423562593
a = 62150203092456938230366891668382702110196631396589305390157506915312399058961554609342345998
b = 1005820216843804918712728918305396768000492821656453232969553225956348680715987662653812284211
F = GF(p)
E.<G> = EllipticCurve(F, [a, b])
assert FLAG < G.order()
k = randrange(G.order())
P = k * G
Q = FLAG * P

res = []
for _ in range(42):
    a = randrange(G.order())
    b = randrange(G.order())
    res.append((a, b, a * P + b * Q))
print(res)
