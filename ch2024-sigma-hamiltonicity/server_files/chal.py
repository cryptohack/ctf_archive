from hamiltonicity import pedersen_commit, pedersen_open
from hamiltonicity import commit_to_graph, open_graph, permute_graph
from hamiltonicity import hash_committed_graph, testcycle, check_graph
from hamiltonicity import comm_params
import json
import os

FLAG = os.environ["FLAG"].encode()

numrounds = 128
LocalTest = False

if LocalTest:
    # Graph with Hamiltonian cycle (0,4) (4,2) (2,3) (3,1) (1,0)
    # You can use this locally to test correct proofs :)
    N = 5
    G = [
        [0,1,1,0,1],
        [1,0,0,0,0],
        [0,0,0,1,0],
        [0,1,1,0,0],
        [1,0,1,1,0]
    ]

else: 
    # Graph with no hamiltonian cycle
    # Break the fiat shamir to convince the server this has a cycle to get the flag :)
    N = 5
    G = [
        [0,0,1,0,0],
        [1,0,0,0,0],
        [0,1,0,0,0],
        [0,0,0,0,1],
        [0,0,0,1,0]
    ]




print(f'prove to me that G has a hamiltonian cycle!')

# 128 bit security
FS_state = b''
for i in range(numrounds):
    # send permuted commitment matrix
    payload = json.loads(input(b"send fiat shamir proof: "))

    A = payload["A"]
    z = payload["z"]
    check_graph(A,N)

    FS_state = hash_committed_graph(A, FS_state, comm_params)
    # take one bit of hash as challenge
    challenge = FS_state[-1] & 1
    
    # Challenge bit is 1:
    # You should open the hamiltonian path
    # z = [cycle, openings of cycle]
    if challenge:
        cycle, openings = z
        if not testcycle(A, N, cycle, openings):
            print("your proof didn't verify :(")
            exit()
        else:
            print("accepted")
    
    # challenge bit is 0:
    # you should show permutation and open everything
    # z = [permutation, openings of everything]
    else:
        permutation, openings = z
        G_permuted = open_graph(A,N, openings)
        G_test = permute_graph(G, N, permutation)
        if G_permuted == G_test:
            print("accepted")
        else:
            print("your proof didn't verify :()")
            exit()
    


print("you've convinced me it has a hamiltonian path! Cool!")
print(FLAG)
