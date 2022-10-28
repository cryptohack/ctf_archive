from gmpy2 import is_prime
import random
import sys
import re
import os

def hash(m):
    m = int.from_bytes(b'SECUREHASH_' + m, 'big')
    return pow(g, m, p).to_bytes(256//8, 'big')

if __name__ == '__main__':
    flag = os.environ.get('FLAG', 'firebird{***REDACTED***}')

    while True:
        g = random.getrandbits(256)
        p = random.getrandbits(256)
        if not is_prime(p): continue
        break

    for _ in range(5):
        m = input().strip()

        if re.match(r'^[a-z]+$', m) is None:
            print('Please be less rude.')
            sys.exit(0) 

        m = m.encode()
        h = hash(m)
        print(f'h({m}) = {h.hex()}')

        if m == b'pleasegivemetheflag':       continue
        if h != hash(b'pleasegivemetheflag'): continue
    
        print(f'Congrats! {flag}')
        sys.exit(0)
