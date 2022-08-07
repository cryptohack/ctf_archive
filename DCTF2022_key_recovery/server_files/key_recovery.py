import os
from hashlib import sha512

FLAG = os.environ.get("FLAG")

BS = 16
R = 3

S_box = [80, 12, 233, 22, 60, 179, 30, 32, 112, 114, 174, 83, 207, 107, 33, 237, 37, 121, 161, 50, 54, 57, 77, 59, 152, 53, 52, 204, 70, 104, 163, 68, 196, 189, 17, 211, 178, 220, 92, 137, 78, 29, 96, 103, 239, 213, 108, 109, 111, 113, 90, 162, 21, 120, 23, 157, 123, 195, 186, 205, 132, 236, 232, 145, 248, 85, 134, 135, 139, 140, 102, 144, 249, 147, 181, 130, 194, 154, 175, 183, 219, 28, 66, 202, 91, 116, 142, 106, 9, 188, 203, 117, 206, 208, 151, 242, 82, 14, 210, 217, 20, 221, 227, 10, 99, 156, 160, 241, 67, 126, 65, 45, 231, 191, 46, 71, 58, 245, 24, 235, 218, 253, 61, 64, 79, 192, 8, 63, 3, 122, 35, 7, 81, 38, 201, 40, 252, 118, 254, 133, 177, 73, 34, 13, 180, 76, 4, 62, 15, 110, 165, 246, 100, 98, 89, 55, 250, 56, 47, 86, 72, 143, 173, 131, 223, 39, 115, 222, 166, 1, 148, 16, 74, 51, 200, 146, 95, 6, 36, 128, 69, 184, 155, 153, 31, 216, 215, 88, 2, 240, 187, 11, 167, 212, 164, 43, 214, 171, 49, 244, 243, 0, 209, 44, 197, 172, 251, 84, 170, 198, 168, 149, 75, 26, 136, 119, 230, 225, 255, 42, 228, 125, 185, 229, 124, 25, 93, 224, 5, 158, 226, 87, 101, 129, 176, 159, 169, 193, 48, 247, 234, 182, 41, 238, 94, 105, 18, 97, 141, 199, 150, 127, 138, 27, 19, 190]
S_box_inv = [201, 169, 188, 128, 146, 228, 177, 131, 126, 88, 103, 191, 1, 143, 97, 148, 171, 34, 246, 254, 100, 52, 3, 54, 118, 225, 213, 253, 81, 41, 6, 184, 7, 14, 142, 130, 178, 16, 133, 165, 135, 242, 219, 195, 203, 111, 114, 158, 238, 198, 19, 173, 26, 25, 20, 155, 157, 21, 116, 23, 4, 122, 147, 127, 123, 110, 82, 108, 31, 180, 28, 115, 160, 141, 172, 212, 145, 22, 40, 124, 0, 132, 96, 11, 207, 65, 159, 231, 187, 154, 50, 84, 38, 226, 244, 176, 42, 247, 153, 104, 152, 232, 70, 43, 29, 245, 87, 13, 46, 47, 149, 48, 8, 49, 9, 166, 85, 91, 137, 215, 53, 17, 129, 56, 224, 221, 109, 251, 179, 233, 75, 163, 60, 139, 66, 67, 214, 39, 252, 68, 69, 248, 86, 161, 71, 63, 175, 73, 170, 211, 250, 94, 24, 183, 77, 182, 105, 55, 229, 235, 106, 18, 51, 30, 194, 150, 168, 192, 210, 236, 208, 197, 205, 162, 10, 78, 234, 140, 36, 5, 144, 74, 241, 79, 181, 222, 58, 190, 89, 33, 255, 113, 125, 237, 76, 57, 32, 204, 209, 249, 174, 134, 83, 90, 27, 59, 92, 12, 93, 202, 98, 35, 193, 45, 196, 186, 185, 99, 120, 80, 37, 101, 167, 164, 227, 217, 230, 102, 220, 223, 216, 112, 62, 2, 240, 119, 61, 15, 243, 44, 189, 107, 95, 200, 199, 117, 151, 239, 64, 72, 156, 206, 136, 121, 138, 218]
P_nib = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
P_box = [24, 19, 12, 25, 0, 9, 6, 31, 26, 11, 28, 5, 14, 13, 20, 15, 18, 21, 10, 27, 4, 1, 22, 3, 8, 17, 16, 29, 2, 23, 30, 7]
P_box_inv = [4, 21, 28, 23, 20, 11, 6, 31, 24, 5, 18, 9, 2, 13, 12, 15, 26, 25, 16, 1, 14, 17, 22, 29, 0, 3, 8, 19, 10, 27, 30, 7]

menu = """What do you want to do?
1 - Encrypt
2 - Decrypt
3 - Get flag
> """

xor = lambda a,b: bytes(x^y for x,y in zip(a,b))

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

def sub(x):
    return bytes([S_box[a] for a in x])

def sub_inv(x):
    return bytes([S_box_inv[a] for a in x])

def per(x):
    x = byte_to_nib(x)
    x = [P_nib[x[P_box[i]]] for i in range(32)]
    return nib_to_byte(x)

def per_inv(x):
    x = byte_to_nib(x)
    x = [P_nib[x[P_box_inv[i]]] for i in range(32)]
    return nib_to_byte(x)

def block(x, keys):
    for r in range(R):
        x = sub(x)
        x = xor(x, keys[r])
        x = per(x)

    x = sub(x)
    x = xor(x, keys[R])

    return x

def block_inv(x, keys):
    x = xor(x, keys[R])
    x = sub_inv(x)

    for i in range(R-1, -1, -1):
        x = per_inv(x)
        x = xor(x, keys[i])
        x = sub_inv(x)

    return x

def enc(k, pt):
    s = key_schedule(k)
    l = len(pt)
    if l % BS:
        pt += b"\0" * (BS - (l % BS))
    return b"".join([block(pt[i:i+BS], s) for i in range(0, l, BS)])

def dec(k, ct):
    s = key_schedule(k)
    l = len(ct)
    return b"".join([block_inv(ct[i:i+BS], s) for i in range(0, l, BS)])

def main():
    cnt = 0
    K = os.urandom(BS)
    print("I bet you can't recover my key, so I made a game for you. You shouldn't need more than 3000 blocks.")

    while True:
        print(menu, end="")
        op = input()
        if op == "1":
            print("Send me the text you want to encrypt in hex format:")
            pt = bytes.fromhex(input())
            cnt += (len(pt) + BS - 1) // BS
            if cnt > 3000:
                print("You can't encrypt that much. Goodbye!")
                break
            ct = enc(K, pt)
            print("Here you go: ", ct.hex())
        elif op == "2":
            print("Send me the text you want to decrypt in hex format:")
            ct = bytes.fromhex(input())
            l = len(ct)
            if l % BS:
                print("This is not a valid ciphertext. Try again.")
                continue
            cnt += l // BS
            if cnt > 3000:
                print("You can't decrypt that much. Goodbye!")
                break
            pt = dec(K, ct)
            print("Here you go: ", pt.hex())
        elif op == "3":
            print("So you want to get the flag? Tell me what my key is in hex format:")
            key = bytes.fromhex(input())
            if key == K:
                print("Congratulations, here you go: ", FLAG)
            else:
                print("You tried, but this is not the key :(")
                break
        else:
            print("Invalid option, exiting...")
            break

main()