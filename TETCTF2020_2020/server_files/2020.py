import os
import random

if __name__ == '__main__':
    print("Pick two indices to reveal, then guess the 2020th number!")

    nIndices = 2
    indices = [int(input()) for _ in range(nIndices)]

    for i in range(2019):
        r = random.getrandbits(32)
        print(r if i in indices else 'Nope!')

    if int(input()) == random.getrandbits(32):
        print(os.environ["FLAG"])
