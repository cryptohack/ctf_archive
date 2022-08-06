import base64
import ed25519
import os
import sys

FLAG = open("flag.txt", "r").read()


def die(*args):
    pr(*args)
    quit()


def pr(*args):
    s = " ".join(map(str, args))
    sys.stdout.write(s + "\n")
    sys.stdout.flush()


def level(i):
    border = "-"
    pr(border*72)
    pr(border, f" Level {i}", border)
    pr(border*72)


def sc():
    return sys.stdin.readline().strip()


def get_keys():
    if os.path.exists("sk.txt") and os.path.exists("vk.txt"):
        with open("sk.txt", "rb") as f:
            sk = f.read()
        with open("vk.txt", "rb") as f:
            vk = f.read()
        signing_key = ed25519.SigningKey(sk)
        verifying_key = ed25519.VerifyingKey(vk)
    else:
        signing_key, verifying_key = ed25519.create_keypair()
        with open("sk.txt", "wb") as f:
            f.write(signing_key.to_bytes())
        with open("vk.txt", "wb") as f:
            f.write(verifying_key.to_bytes())
    return signing_key, verifying_key


def verify(verifying_key, sig, msg):
    try:
        verifying_key.verify(sig, msg, encoding="base64")
        print("signature is good")
    except ed25519.BadSignatureError:
        print("signature is bad!")


def main():
    level(1)

    signing_key, verifying_key = get_keys()
    msg = b"CryptoHack"
    sig = signing_key.sign(msg)

    pr("Signature:")
    pr(base64.b64encode(sig).decode())
    pr("Enter new signature:")
    new_sig = base64.b64decode(sc())
    if new_sig == sig:
        die("Same signature")

    try:
        verifying_key.verify(new_sig, msg)
    except Exception:
        die("Signature is bad!")

    level(2)

    msg = os.urandom(16)

    pr("Enter verifying key:")
    vk = base64.b64decode(sc())
    pr("Enter signature:")
    sig = base64.b64decode(sc())

    try:
        verifying_key = ed25519.VerifyingKey(vk)
    except Exception:
        die("Key is bad!")
    try:
        verifying_key.verify(sig, msg)
    except Exception:
        die("Signature is bad!")

    die(FLAG)


if __name__ == '__main__':
    main()
