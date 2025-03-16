from json import dumps, loads
from gcm import GCM, IV_LEN

IV  = b"\x00"*IV_LEN

def build_token(key, username, role):
    gcm = GCM(key, IV)
    token = dumps({
        "username": username,
        "role": role
    }).encode()

    ct, tag = gcm.encrypt(token)
    return ";".join([ct.hex(), tag.hex()])

def verif_token(key, token):
    gcm = GCM(key, IV)
    ct, tag = [bytes.fromhex(a) for a in token.split(";")]
    pt, is_auth = gcm.decrypt(ct, tag)

    if loads(pt.decode())["role"] != "super_admin":
        return False

    return True

