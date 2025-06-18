load("parameters.sage")
from base64 import b64encode, b64decode
from ast import literal_eval
import gzip

def sanitize_mat(A):
    A = [[list(AAA) for AAA in AA] for AA in A]
    A = str(A).replace(" ", "")
    A = A.encode()

    return b64encode(gzip.compress(A)).decode()

def sanitize_vec(u):
    u = [list(uu) for uu in u]
    u = str(u).replace(" ", "")
    u = u.encode()

    return b64encode(gzip.compress(u)).decode()

def isanitize_mat(s):
    s = b64decode(s)
    s = gzip.decompress(s)
    s = literal_eval(s.decode())

    return Matrix(Rq, [[Rq(sss) for sss in ss] for ss in s])

def isanitize_vec(s):
    s = b64decode(s)
    s = gzip.decompress(s)
    s = literal_eval(s.decode())

    return vector(Rq, [Rq(ss) for ss in s])

