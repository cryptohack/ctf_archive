import os
from hashlib import sha512
from pwn import remote, xor

HOST = "127.0.0.1"
PORT = 1337

io = remote(HOST, PORT)

BS = 16
R = 3

S_box_inv = [201, 169, 188, 128, 146, 228, 177, 131, 126, 88, 103, 191, 1, 143, 97, 148, 171, 34, 246, 254, 100, 52, 3, 54, 118, 225, 213, 253, 81, 41, 6, 184, 7, 14, 142, 130, 178, 16, 133, 165, 135, 242, 219, 195, 203, 111, 114, 158, 238, 198, 19, 173, 26, 25, 20, 155, 157, 21, 116, 23, 4, 122, 147, 127, 123, 110, 82, 108, 31, 180, 28, 115, 160, 141, 172, 212, 145, 22, 40, 124, 0, 132, 96, 11, 207, 65, 159, 231, 187, 154, 50, 84, 38, 226, 244, 176, 42, 247, 153, 104, 152, 232, 70, 43, 29, 245, 87, 13, 46, 47, 149, 48, 8, 49, 9, 166, 85, 91, 137, 215, 53, 17, 129, 56, 224, 221, 109, 251, 179, 233, 75, 163, 60, 139, 66, 67, 214, 39, 252, 68, 69, 248, 86, 161, 71, 63, 175, 73, 170, 211, 250, 94, 24, 183, 77, 182, 105, 55, 229, 235, 106, 18, 51, 30, 194, 150, 168, 192, 210, 236, 208, 197, 205, 162, 10, 78, 234, 140, 36, 5, 144, 74, 241, 79, 181, 222, 58, 190, 89, 33, 255, 113, 125, 237, 76, 57, 32, 204, 209, 249, 174, 134, 83, 90, 27, 59, 92, 12, 93, 202, 98, 35, 193, 45, 196, 186, 185, 99, 120, 80, 37, 101, 167, 164, 227, 217, 230, 102, 220, 223, 216, 112, 62, 2, 240, 119, 61, 15, 243, 44, 189, 107, 95, 200, 199, 117, 151, 239, 64, 72, 156, 206, 136, 121, 138, 218]
P_nib = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
P_box_inv = [4, 21, 28, 23, 20, 11, 6, 31, 24, 5, 18, 9, 2, 13, 12, 15, 26, 25, 16, 1, 14, 17, 22, 29, 0, 3, 8, 19, 10, 27, 30, 7]

def nib_to_byte(x):
    return bytes([x[i]*16 + x[i+1] for i in range(0,len(x), 2)])

def byte_to_nib(x):
    out = []
    for b in x:
        out.append(b//16)
        out.append(b%16)
    return out

def key_schedule(k):
    k += sha512(k).digest()
    return [k[i:i+BS] for i in range(0,(R+1)*BS, BS)]

def sub_inv(x):
    return bytes([S_box_inv[a] for a in x])

def per_inv(x):
    x = byte_to_nib(x)
    x = [P_nib[x[P_box_inv[i]]] for i in range(32)]
    return nib_to_byte(x)



def send(op, payload):
    io.sendlineafter(b">", op)
    io.sendlineafter(b":\n", payload.hex())
    tmp = io.recvline().decode().strip().split()[-1]
    return tmp

def prepare_pairs(n, a):
    pairs = []
    for _ in range(n):
        try:
            x = os.urandom(16)
            k = send("1",x)
            y = unhex(k)
            x_a = xor(x, a)
            k_a = send("1",x_a)
            y_a = unhex(k_a)
            pairs.append((y,y_a))
        except:
            print(k,k_a)
            exit()
    return pairs

mask = b'\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe'

pairs = prepare_pairs(1499, mask)

def get_key(pairs):
    for i in range(R+1):
        key = []

        for j in range(16):
            candidates = [0] * 256
            for pair in pairs:
                y  = pair[0][j]
                y_ = pair[1][j]
                
                for k in range(256):
                    xor_y = y ^ k
                    xor_y_ = y_ ^ k
                    rev_y = S_box_inv[xor_y]
                    rev_y_ = S_box_inv[xor_y_]
                    if rev_y ^ rev_y_ == mask[j]:
                        candidates[k] += 1
            key.append(candidates.index(max(candidates)))

        for i in range(len(pairs)):
            x,y = pairs[i]
            x = xor(x, key)
            x = sub_inv(x)
            x = per_inv(x)
            y = xor(y, key)
            y = sub_inv(y)
            y = per_inv(y)
            pairs[i] = (x,y)
        print(bytes(key))
    return bytes(key)

key = get_key(pairs)
print(send("3",key))