"""
I’m using the level 5 parameters of ML-DSA (f.k.a CRYSTALS-Dilithium) [1],  
as recommended by ANSSI [2]. Nothing can happen to me, right?

[1] : https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf
[2] : https://cyber.gouv.fr/publications/avis-de-lanssi-sur-la-migration-vers-la-cryptographie-post-quantique-0
"""

RING_RANK = 256
q = 8380417 # 2^23 - 2^13 + 1
k, l = 8, 7
eta = 2

Fq = GF(q)
base_ring.<x> = Fq[]
Rq.<X> = base_ring.quotient_ring(x^RING_RANK - 1)

