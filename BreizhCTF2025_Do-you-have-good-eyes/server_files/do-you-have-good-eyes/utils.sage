load("parameters.sage")

from secrets import SystemRandom
rng = SystemRandom()

def rnd_elem(R, b):
    P = []

    for _ in range(RING_RANK):
        P.append(rng.randrange(-b, b+1))

    return R(P)

def rnd_vec(R, dim, b):
    u = []

    for _ in range(dim):
        u.append(rnd_elem(R, b))

    return vector(u)

def get_instance():
    is_mlwe = rng.getrandbits(1)

    A = random_matrix(Rq, k, l)
    s = rnd_vec(Rq, l, eta)
    e = rnd_vec(Rq, k, eta)

    t = A*s + e
    r = random_vector(Rq, k)

    from time import sleep
    sleep(rng.random()/5)

    if is_mlwe:
        return (A, t), is_mlwe
    else:
        return (A, r), is_mlwe

