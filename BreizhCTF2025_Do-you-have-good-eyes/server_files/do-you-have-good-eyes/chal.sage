load("sanitize.sage")
load("utils.sage")

from os import getenv
FLAG = getenv("FLAG", "BZHCTF{censored}")

print("Hi, I hope you have good eyes !")

count = 0
threshold = 128
for i in range(130):
    if count >= threshold:
        print(f"Well played, here is the flag : {FLAG}")
        exit()

    (A, t), is_mlwe = get_instance()

    print(f"{sanitize_mat(A) = }")
    print(f"{sanitize_vec(t) = }")

    ans = int(input("MLWE (1) or not (0) ?\n> "))

    if ans == is_mlwe:
        count += 1
        print(f"wp, {count}/{threshold}")
    else:
        print(f"oups, {count}/{threshold}")

