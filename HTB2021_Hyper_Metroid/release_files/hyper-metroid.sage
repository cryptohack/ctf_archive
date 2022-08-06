from secrets import flag

def alien_prime(a):
	p = (a^5 - 1) // (a - 1)
	assert is_prime(p)
	return p


def encrypt_flag():
	e = 2873198723981729878912739
	Px = int.from_bytes(flag, 'big')
	P = C.lift_x(Px)
	JP = J(P)
	return e * JP


def transmit_point(P):
	mumford_x = P[0].list()
	mumford_y = P[1].list()
	return (mumford_x, mumford_y)


a = 1152921504606846997
alpha = 1532495540865888942099710761600010701873734514703868973
p = alien_prime(a)

FF = FiniteField(p)
R.<x> = PolynomialRing(FF)

h = 1
f = alpha*x^5

C = HyperellipticCurve(f,h,'u,v')
J = C.jacobian()
J = J(J.base_ring())

enc_flag = encrypt_flag()

print(f'Encrypted flag: {transmit_point(enc_flag)}')
