# Origami (NNS CTF 2025) - NTRU key recovery by folding
#
# The public key lives in Z_q[x]/(x^n - 1) with n = 512, and x^n - 1 is divisible by x^k - 1 for
# every k | n. Reducing mod x^k - 1 "folds" a polynomial: coefficient i becomes the sum of the
# coefficients at i, i + k, i + 2k, ... Folding keeps f and g short and non-negative (their
# coefficients still sum to df = dg = 35) and keeps h = g/f true, so:
#
#  1. At k = 64 the folded key lies in a short, dense sublattice of a 128-dimensional NTRU lattice.
#     BKZ finds that sublattice; the folded key is its shortest vector whose coefficients sum to 35.
#  2. Unfold one level at a time. If F = f mod (x^k - 1) is known, then f mod (x^2k - 1) = (A, F - A)
#     for an unknown A with 0 <= A_i <= F_i, and A_i = 0 wherever F_i = 0. Only ~35 unknowns remain,
#     so a small embedding lattice recovers A even at the top level (k = 256 -> 512).
#  3. With the full f, decrypt as normal: m = (f * c mod q) / f mod 2.
#
# The key is only ever recovered up to a rotation x^j * f, which is an equally valid decryption key.
import sys

n, p, q, df, dg = 512, 2, 127, 35, 35
exec(open(sys.argv[1] if len(sys.argv) > 1 else "output.txt").read())
# coefficients(sparse=False) drops trailing zero coefficients, so pad back up to n
# (losing more than a few would be astronomically unlikely, so anything shorter is a broken output file)
assert n - 8 <= len(pk) <= n and n - 8 <= len(ct) <= n, f"expected {n} coefficients, got {len(pk)} and {len(ct)}"
pk, ct = pk + [0] * (n - len(pk)), ct + [0] * (n - len(ct))


def folded_circulant(k):
    """Matrix whose row i holds x^i * (h mod x^k - 1), so (row vector f) * H = f * h."""
    hk = [sum(pk[i::k]) % q for i in range(k)]
    return matrix.circulant(hk)


def is_folded_key(f, H, k):
    """f must look like a fold of the real key, and f * h must look like a fold of g."""
    g = [ZZ(v) % q for v in vector(ZZ, f) * H]
    top = n // k
    return (all(0 <= v <= top for v in f) and sum(f) == df
            and all(0 <= v <= top for v in g) and sum(g) == dg)


def base_candidates(k):
    """Folded keys at level k via the standard NTRU lattice [[I, H], [0, qI]].

    Reduction finds the k-dimensional dense sublattice containing the rotations x^j * (F, G), but
    its shortest vectors are usually not F itself: they are pieces such as F - x^j F, or fragments of
    F (x^k - 1 is reducible, so the sublattice also holds "fractions" of the key). The rotations are
    the short vectors whose coefficients sum to exactly 35. So split the sublattice into its sum-zero
    part plus one vector of sum 35, and solve that CVP by embedding to find the shortest such vector."""
    H = folded_circulant(k)
    L = block_matrix(ZZ, [[identity_matrix(k), H], [zero_matrix(k), q * identity_matrix(k)]])
    B = L.BKZ(block_size=20)
    # short vectors of the dense sublattice satisfy sum(f) == sum(g) exactly, because h(1) = 1
    dense = [r for r in B.rows() if any(r) and sum(r[:k]) == sum(r[k:])][:k]
    if len(dense) < k:
        return
    D = matrix(ZZ, dense)
    sums = matrix(ZZ, [[sum(r[:k])] for r in dense])
    E, U = sums.echelon_form(transformation=True)  # U * sums = (gcd, 0, ..., 0)
    if E[0, 0] == 0 or df % E[0, 0]:
        return
    v = (df // E[0, 0]) * U[0] * D  # a vector of the sublattice with coefficient sum 35
    D0 = U[1:] * D  # the sum-zero part of the sublattice
    emb = block_matrix(ZZ, [[D0, zero_matrix(k - 1, 1)], [v.row(), identity_matrix(1)]])
    for row in emb.BKZ(block_size=20):
        if abs(row[-1]) == 1:
            f = list(row[:k] * row[-1])
            if is_folded_key(f, H, k):
                yield f


def unfold(F):
    """Given F = f mod (x^k - 1), recover f mod (x^2k - 1) = (A, F - A)."""
    k = len(F)
    H = folded_circulant(2 * k)
    support = [i for i in range(k) if F[i] > 0]
    cols = list(range(k))  # g has 2k coefficients; k of them are plenty of constraints
    # g = (A, F - A) * H = A * (H_top - H_bottom) + (0, F) * H
    diff = (H[:k] - H[k:])[support, cols]
    offset = vector(ZZ, [0] * k + list(F)) * H
    offset = vector(ZZ, [offset[j] % q for j in cols])
    s, c = len(support), len(cols)
    L = block_matrix(ZZ, [
        [identity_matrix(s), diff, zero_matrix(s, 1)],
        [zero_matrix(1, s), offset.row(), identity_matrix(1)],
        [zero_matrix(c, s), q * identity_matrix(c), zero_matrix(c, 1)],
    ])
    for row in L.BKZ(block_size=20):
        if abs(row[-1]) != 1:
            continue
        row = row * row[-1]  # make the embedding coordinate +1
        A = [0] * k
        for idx, i in enumerate(support):
            A[i] = row[idx]
        f = A + [F[i] - A[i] for i in range(k)]
        if is_folded_key(f, H, 2 * k):
            return f
    return None


def recover_key(start=64):
    for F in base_candidates(start):
        print(f"[+] level {start}: folded key candidate found")
        k = start
        while F is not None and len(F) < n:
            F = unfold(F)
            k *= 2
            if F is not None:
                print(f"[+] level {k}: unfolded")
        if F is not None:
            return F
    raise ValueError("key recovery failed")


f = recover_key()
assert set(f) <= {0, 1} and sum(f) == df

Rq.<x> = PolynomialRing(Zmod(q))
Rp.<w> = PolynomialRing(Zmod(p))
a = (Rq(f) * Rq(ct)) % (x ^ n - 1)
a = [ZZ(v) if ZZ(v) <= q // 2 else ZZ(v) - q for v in a.list()]  # centre-lift: now exact over Z
m = (Rp(a) * Rp(f).inverse_mod(w ^ n - 1)) % (w ^ n - 1)
val = sum(int(bit) << i for i, bit in enumerate(m.list()))
print(val.to_bytes((val.bit_length() + 7) // 8, "big").decode())
