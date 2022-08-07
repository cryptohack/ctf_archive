import random
from Crypto.Util.number import getPrime as get_prime

# https://link.springer.com/content/pdf/10.1007/s42452-019-1928-8.pdf
class NagatyCryptosystem:
    def __init__(self, p=None):
        # Section 3.1
        # "Select a very large prime number p."
        self.p = get_prime(1024) if p is None else p
        
        # Generate 1024 numbers as the sequence
        u = [random.getrandbits(1024) for _ in range(1024)]

        self.private_key = sum(u)
        self.public_key  = self.private_key % self.p

        self.shared_key = None

    def start_exchange(self):
        return (self.public_key, self.p)

    def exchange(self, y_B):
        S_A = self.private_key
        y_A = self.public_key

        y_AB = y_A * y_B
        S_AB = (y_AB * y_B) * S_A % self.p

        self.shared_key = S_AB

    def encrypt(self, m):
        sk = self.shared_key
        if sk is None: raise Exception('Key exchange is not completed')

        return m * sk
    
    def decrypt(self, c):
        sk = self.shared_key
        if sk is None: raise Exception('Key exchange is not completed')

        return c // sk


# Sanity test
def test():
    cipher_alice = NagatyCryptosystem()
    alice_public_key, p = cipher_alice.start_exchange()

    cipher_bob = NagatyCryptosystem(p)
    bob_public_key, _ = cipher_bob.start_exchange()

    cipher_alice.exchange(bob_public_key)
    cipher_bob.exchange(alice_public_key)

    # Test: Alice sends a message to Bob and Bob is able to decrypt it
    m = 1337
    c = cipher_alice.encrypt(m)
    assert cipher_bob.decrypt(c) == m

    # Test: Bob sends a message to Alice and Alice is able to decrypt it
    m = 1337
    c = cipher_bob.encrypt(m)
    assert cipher_alice.decrypt(c) == m

def main():
    # Reads the flag and converts the string into a number
    with open('flag.txt', 'rb') as f: flag = f.read()
    flag = int.from_bytes(flag, 'big')

    cipher_alice = NagatyCryptosystem()
    alice_public_key, p = cipher_alice.start_exchange()

    cipher_bob = NagatyCryptosystem(p)
    bob_public_key, _ = cipher_bob.start_exchange()

    cipher_alice.exchange(bob_public_key)
    cipher_bob.exchange(alice_public_key)

    c = cipher_alice.encrypt(flag)
    
    print('p =', hex(p))
    print('y_A =', hex(alice_public_key))
    print('y_B =', hex(bob_public_key))
    print('c =', hex(c))

if __name__ == '__main__':
    test()
    main()