from Crypto.Util.number import getPrime, isPrime, bytes_to_long
import string, signal, random, hashlib, os
signal.alarm(1500)

def gen_pow():
    print("Solve PoW plz")
    s = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    print(s)
    answer = input()
    hash = bytes_to_long(hashlib.sha256((s + answer).encode()).digest())
    if hash != (hash >> 26) << 26:
        exit() 

gen_pow()
q = getPrime(342)
print("q = {}".format(q))

class LCG:
    def __init__(self, a, x, b):
        self.a = a
        self.x = x 
        self.b = b 
    def fetch(self):
        ret = self.x
        self.x = (self.a * self.x + self.b) % q 
        return ret 
    
print("Hello! You are the owner of one Share Generator! Please insert your parameters :)")
a = int(input()) % q
x = int(input()) % q
b = int(input()) % q

assert 1 <= a < q and 1 <= x < q and 1 <= b < q 

LCG1 = LCG(a, x, b)
LCG2 = LCG(random.randint(1, q-1), random.randint(1, q-1), random.randint(1, q-1))
LCG3 = LCG(random.randint(1, q-1), random.randint(1, q-1), random.randint(1, q-1))

def roll():
    return LCG3.fetch() * q * q + LCG2.fetch() * q + LCG1.fetch()

def checkFactor(n):
    u = int(input())
    v = int(input())
    assert 1 < u < n and 1 < v < n and u * v == n

pr = []

while len(pr) < 8:
    p = roll()
    if isPrime(p):
        pr.append(p)

n1 = pr[0] * pr[1]
n2 = pr[2] * pr[3]
n3 = pr[4] * pr[5]
n4 = pr[6] * pr[7]

print(n1)
print(n2)
print(n3)
print(n4)

checkFactor(n1)
checkFactor(n2)
checkFactor(n3)
checkFactor(n4)

flag = os.environ.get("FLAG")
print(flag)