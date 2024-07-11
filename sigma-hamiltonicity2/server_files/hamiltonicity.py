import random
from Crypto.Util.number import isPrime
from hashlib import sha256

P = 0x19dad539e2d348cc3ab07d51f2bb6491d1552aa8cf1db928920fd3d86946aed8805d2e279fa8632dd5fbab8aaf7df1069906b057cc785b7f191ef1b9b5da38cff2e7c64da17bb56a058707d9fd69e546a95e502e556a314c587c7ae36c3d1122e6954f5d81dd9239e02f61b045360187b4caeed271cec1919a0d8a39e855040cf
q = 0xced6a9cf169a4661d583ea8f95db248e8aa9554678edc944907e9ec34a3576c402e9713cfd43196eafdd5c557bef8834c83582be63c2dbf8c8f78dcdaed1c67f973e326d0bddab502c383ecfeb4f2a354af28172ab518a62c3e3d71b61e8891734aa7aec0eec91cf017b0d8229b00c3da65776938e760c8cd06c51cf42a82067


# Generate `h1,h2` to be a random element Z_P of order q
# Unknown dlog relation is mask for the Pedersen Commitment

# Hardcoded a random `h1,h2` value for ease of use
# h1 = pow(random.randint(2,P-1),2,P)
# h2 = pow(random.randint(2,P-1),2,P)
h1 = 250335104192448110684442096964171969189371208477846978499544515755228857598805930673171509152681305793789903169450438090936970626429806187630240086681623358732517929314870247393468568111513100989768455673769015138136779312483203922847547169463972757664497001482465636402329003817055202840451714256443734563502
h2 = 50837518481371967588098771977165879422445597094015682347125264774697010574110399136037637691883034517374621248070926110725252171239208140392324019115211573768989274797050961703999139947885402838647962534519882622024973824201026885393782961783980351898031905383197219266093119145616328556294476943229578292306
comm_params = P,q,h1,h2



# Information theoretically hiding commitment scheme
def pedersen_commit(message, pedersen_params = comm_params):
    P,q,h1,h2 = pedersen_params
    r = random.randint(0,q)
    commitment = (pow(h1,message,P) * pow(h2,r,P)) % P
    return commitment, r

def pedersen_open(commitment,message,r, pedersen_params = comm_params):
    P,q,h1,h2 = pedersen_params
    if (commitment * pow(h1,-message,P) * pow(h2,-r,P) ) % P == 1:
        return True
    else:
        return False

# Given a graph, return an element-wise commitment to the graph
def commit_to_graph(G,N):
    G2 = [[0 for _ in range(N)] for _ in range(N)]
    openings = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = G[i][j]
            comm, r = pedersen_commit(v)
            assert pedersen_open(comm,v,r)
            G2[i][j] = comm
            openings[i][j] = [v,r]
    return G2, openings

def check_graph(G,N):
    assert len(G) == N, "G has wrong size"
    for r in G:
        assert len(r) == N, "G has wrong size"
    return True

# Takes a commitment to a graph, and opens all the commitments to reveal the graph
def open_graph(G2,N, openings):
    G = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = G2[i][j]
            m,r = openings[i][j]
            assert pedersen_open(v, m, r)
            G[i][j] = m
    return G


# Takes a commitment to a graph, and a claimed set of entries which should open a hamiltonian cycle
# Returns True if the opened nodes form a hamiltonian cycle
def testcycle(graph, N, nodes, openings):
    assert len(nodes) == N
    from_list = [n[0] for n in nodes]
    to_list = [n[1] for n in nodes]
    for i in range(N):
        assert i in from_list
        assert i in to_list
        assert nodes[i][1] == nodes[(i+1)%N][0]

    for i in range(N):
        src,dst = nodes[i]
        r = openings[i]
        # print(f'trying to open {src}->{dst} {r} {graph[src][dst]}')
        assert pedersen_open(graph[src][dst], 1, r)
    return True

# Given a graph, and a permutation, shuffle the graph using the permutation
def permute_graph(G, N, permutation):
    G_permuted = [[G[permutation[i]][permutation[j]] for j in range(N)] for i in range(N)]
    return G_permuted

# given a set of commitment private values, and a subset of these indexes
# return a vector of the randomness needed to open the commitments.
def get_r_vals(openings,N, cycle):
    rvals = []
    for x in cycle:
        m,r = openings[x[0]][x[1]]
        rvals.append(r)
    return rvals


# Iterated Fiat Shamir, take previous state and current graph
def hash_committed_graph(G, state, comm_params):
    fs_state = sha256(str(comm_params).encode())
    fs_state.update(state)
    first_message = "".join([str(x) for xs in G for x in xs])
    fs_state.update(first_message.encode())
    iterated_state = fs_state.digest()
    return iterated_state 
