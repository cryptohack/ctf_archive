from pwn import remote
import itertools
import struct

p = 17585255163044402023

R.<x> = GF(p)[]
L = GF(p).algebraic_closure()

#r = remote("0.0.0.0",int(1337))
r = remote("courbe.ctf.bzh",int(30013))

flag = bytes.fromhex(r.recvline().decode())

pts = []

while len(pts) < 16:
	r.recvline()
	r.sendline(b"00"*8*7*2)
	d = bytes.fromhex(r.recvline().decode())
	blocks = [d[i:i+8] for i in range(0, len(d[:8*7]), 8)]
	ui = [int.from_bytes(r, 'little') for r in blocks]
	u = x^7 + sum(val*x^(i) for i,val in enumerate(ui))

	roots = [r[0] for r in u.change_ring(L).roots()]

	blocks = [d[i+8*7:i+8*7+8] for i in range(0, len(d[8*7:]), 8)]
	vi = [int.from_bytes(r, 'little') for r in blocks]
	v = sum(val*x^(i) for i,val in enumerate(vi))
	
	for root in roots:
		if "^4" in str(root):
			continue
		pts.append((root,v(root)**2))
	print("*"*30)

print("Points collected")

RR.<zz> = PolynomialRing(L)
f = RR.lagrange_polynomial(pts)
f = sum(int(coeff.as_finite_field_element()[1])*x^i for i,coeff in enumerate(f.coefficients()))
C = HyperellipticCurve(f, 0)
print(C)
J = C.jacobian()

flag, known = flag[:-56], flag[-56:]

known = bytes([c^^d for c,d in zip(known,b" This is your final boss, enjoy it while you still can:)")])

blocks = [known[i:i+8] for i in range(0, len(known), 8)]
vi = [int.from_bytes(r, 'little') for r in blocks]
v = sum(val*x^(i) for i,val in enumerate(vi))

factors = list((v^2 - f).change_ring(R).factor()) + [(1,1)]*3

print(f"got {len(factors)} factors")

for factor in itertools.combinations(factors,4):
	u = prod([fac[0] for fac in factor])
	try:
		rs = [int(u[i]) for i in range(7)]
		keystream = struct.pack('<'+'Q'*len(rs), *rs)
		flog = bytes([c^^d for c,d in zip(keystream,flag)])
		if b"BZH" in flog:
			print(flog)
			break
	except Exception as e:
		print(u,e)
		continue