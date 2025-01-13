#!/usr/bin/env sage
from random import SystemRandom
from hashlib import sha256
from json import loads, dumps
import traceback

flag = os.getenv('FLAG', 'ECSC{redacted}')

def intify(x):
    return list(map(int, x))

def strify(x):
    return list(map(str, x))

class BN:
    # Implements a randomly generated Barreto-Naehrig curve over a prime field of 128 bits.

    # This curve has 64 bits of standard EC dlog security
    # and > 82 bits of F_p^k dlog security.

    # There aren't (intended) vulns here.

    def __init__(self):
        self.p      = 239019556058548081539763731767358519973
        self.Fp     = GF(self.p)
        self.b      = 11
        self.EFp    = EllipticCurve(self.Fp, [0, self.b])
        self.O_EFp  = self.EFp([0, 1, 0])
        self.G1     = self.EFp((1, 133660577740454676305948404600566797994))
        self.t      = self.EFp.trace_of_frobenius()
        self.n      = self.EFp.order()
        self.k      = 12
        self.bits   = ZZ(self.p).nbits()
        self.bytes  = ceil(self.bits/8)

        Fp2.<a>     = GF(self.p^2)
        self.Fp2    = Fp2
        self.eps    = 50853858759521010453592688907791911225*a + 156893423039651253351316307339945502422
        self.EFp2   = EllipticCurve(self.Fp2, [0, self.b/self.eps])
        self.O_EFp2 = self.EFp2([0, 1, 0])
        self.G2     = self.EFp2((100774561144590475569157120930767342387*a + 218728496724280042701446122970647661523, 115367896606755692925113233629944781384*a + 211093354487559124632805793736258741445))
        self.h      = self.EFp2.order()//self.n

        Fp2u.<u>    = self.Fp2[]
        Fp12.<z>    = (u^6 - self.eps).root_field()
        self.Fp2u   = Fp2u
        self.Fp12   = Fp12
        self.z      = z
        self.EFp12  = EllipticCurve(self.Fp12, [0, self.b])

    def phi(self, P):
        assert P in self.EFp2 and P != self.O_EFp2 and self.n*P == self.O_EFp2, f'Point {P} not in <G2>'
        Px, Py = P.xy()
        return self.EFp12(self.z^2 * Px, self.z^3 * Py)
    
    def e(self, P, Q):
        assert P in self.EFp  and P != self.O_EFp, f'Point {P} not in <G1>'
        assert Q in self.EFp2 and Q != self.O_EFp2 and self.n*Q == self.O_EFp2, f'Point {Q} not in <G2>'
        return self.EFp12(P).ate_pairing(self.phi(Q), self.n, self.k, self.t, self.p)
    
class PKG:
    # Implements the Private Key Generator entity,
    # a centralised thingy that generates and distributes
    # user keys for this scheme.

    # There aren't (intended) vulns here.

    def __init__(self):
        self.curve = BN()
        self.r = SystemRandom()
        self.p = self.curve.n

        self._s, self.u = [self.rng() for _ in range(2)]
        self.P_G1 = self.u  * self.curve.G1
        self.P_G2 = self.u  * self.curve.G2
        self.Q    = self._s * self.P_G1

        self.params = {
            # G1 elements
            'P_G1' : intify(self.P_G1.xy()),
            'Q'    : intify(self.Q.xy()),

            # G2 element
            'P_G2' : strify(self.P_G2.xy()),
        }

        print('### broadcasting public parameters ###')
        print(dumps(self.params), '\n')

    def rng(self):
        return int(self.r.randrange(self.p))
    
    def H(self, x):
        return int.from_bytes(sha256(x).digest()[:self.curve.bytes], 'big') % self.p
    
    def H0(self, uid):
        x0 = int.from_bytes(sha256(uid.encode()).digest(), 'big') % self.curve.p
        while 1:
            x0 += 1
            try:
                P = self.curve.h * self.curve.EFp2.lift_x(x0)
                if P != self.curve.O_EFp2 and self.p * P == self.curve.O_EFp2:
                    return P
            except:
                continue
    
    def extract(self, uid):
        Qid = self.H0(uid)
        du0 = self._s * Qid
        du1 = int(pow(self._s, -1, self.p)) * Qid
        return (du0, du1), Qid
    
class User:
    def __init__(self, pkg, uid):
        self.curve = pkg.curve
        self.p     = pkg.p
        self.rng   = pkg.rng
        self.H     = pkg.H

        self.P_G1, self.Q = [self.curve.EFp(pkg.params[k])  for k in ['P_G1', 'Q']]
        self.P_G2         =  self.curve.EFp2(pkg.params['P_G2'])

        self.sk, self.Qid = pkg.extract(uid)
        self.verifying = False

    def sign(self, m):
        k = self.rng()
        R = k * self.P_G1
        S = int(pow(k, -1, self.p)) * self.sk[0] + self.H(m.encode()) * self.sk[1]
        R, S = intify(R.xy()), strify(S.xy())
        return (R, S)
    
    def init_verification(self, role, sig, m, Qid_signer):
        self.role, self.verification_step = role.lower(), 0
        self.x, self.y, self.y_inv = None, None, None
        self.sig = {'R': self.curve.EFp(sig[0]), 'S': self.curve.EFp2(sig[1]), 'm': m.encode(), 'Qid': Qid_signer}
        self.verifying = True
        return

    def verify(self, **kwargs):
        assert self.verifying

        if self.role == 'verifier':
            if self.verification_step == 0:
                self.x, self.y = [self.rng() for _ in range(2)]
                self.y_inv = int(pow(self.y, -1, self.p))
                C = self.x * self.y * self.sig['R']
                C = intify(C.xy())
                self.verification_step += 1
                return C

            elif self.verification_step == 1:
                assert 't' in kwargs and 'r' in kwargs
                t, r = kwargs['t'], kwargs['r']
                t, r = list(map(self.curve.Fp12, [t, r]))

                if t != 1 and (t ^ self.p) == 1 and r != 1 and (r ^ self.p) == 1:
                    lhs0 = self.curve.e(self.sig['R'], self.sig['S']) ^ self.x
                    rhs0 = self.curve.e(self.Q, self.sig['Qid']) ^ self.x * \
                        r ^ (self.H(self.sig['m']) * self.y_inv)
                    
                    lhs1 = r ^ self.y_inv * \
                        t ^ self.x     * \
                        self.curve.e(self.P_G1, self.sig['Qid']) ^ self.x
                    rhs1 = self.curve.e(self.sig['R'] + self.Q, self.P_G2) ^ self.x

                    self.verifying = False
                    if lhs0 == rhs0 and lhs1 == rhs1:
                        return True
                return False

        elif self.role == 'signer':
            assert 'C' in kwargs
            C = self.curve.EFp(kwargs['C'])
            t = self.curve.e(self.sig['R'] + self.Q, self.P_G2 - self.sk[1])
            r = self.curve.e(C, self.sk[1])
            t, r = strify([t, r])
            self.verifying = False
            return t, r

pkg = PKG()
admin = User(pkg, 'admin')

try:
    uname = input('tell me your username: ')
    if uname.lower() == 'admin':
        raise Exception('no pls')

    user = User(pkg, uname)
    print(f'thanks! here\'s your private key:')
    print(dumps(strify(user.sk[0].xy())))
    print(dumps(strify(user.sk[1].xy())))

    target = f'I, the eternal Admin, keeper of all secrets, hereby decree that you, {uname}, are worthy to glimpse my deepest and most ancient secret: the flag.'

    R, S = loads(input('give me a signature to verify: '))
    m = input('what message corresponds to this signature? ')
    uname1 = input('who signed it? ')
    
    admin.init_verification('verifier', (R, S), m, pkg.H0(uname1))
    print(f'C = {dumps(admin.verify())}')
    t, r = loads(input('t, r? '))
    result = admin.verify(t=t, r=r)

    match result, uname1, m == target:
        case True, 'admin', True:
            print(flag)
        case True, _, _:
            print('yep, yep, checks out')
        case False, _, _:
            print('oh noes')

except Exception as exc:
    # print(traceback.format_exc())
    print(f'something went wrong! {exc = }')
