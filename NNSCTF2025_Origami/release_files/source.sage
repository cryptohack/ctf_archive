from Crypto.Util.number import bytes_to_long, long_to_bytes

n,p,q,df,dg,dr=[512,2,127,35,35,22]
R.<x>  = ZZ[]
Rq.<x> = Integers(q)[]
Rqn = Rq.quotient(x^n-1)
Rp.<w> = Integers(p)[]
Rpn = Rp.quotient(w^n-1)

def random_poly(d):
    f = R(0)
    for i in sample(range(n),d):
        f += R(x**i)
    return f

def secretkey_gen():
    f,g = [0,0]
    while not Rpn(f).is_unit() or not Rqn(f).is_unit():
        f = random_poly(df)
        g = random_poly(dg)
    return f,g

def publickey_gen(f,g):
    h = Rqn(g)/Rqn(f)
    return h

def encrypt(h,m):
    r = random_poly(dr)
    c = p * h * Rqn(r) + Rqn(m)
    return c
    
def encode(val):
    poly = R(0)
    for i in range(n):
        poly += (val & 1) * x^i
        val >>= 1
    return poly

f,g = secretkey_gen()
pk = publickey_gen(f,g)

flag = encode(bytes_to_long(b"NNS{???????????????????????????????????????????????}"))
ct = encrypt(pk,flag)

print(f"pk = {pk.lift().coefficients(sparse=False)}")
print(f"ct = {ct.lift().coefficients(sparse=False)}")