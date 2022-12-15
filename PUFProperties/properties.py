# Verify Properties of the PUF

from math import log2
from scipy.spatial.distance import hamming


def hammingDistance(list1, list2):
    return list1 ^ list2


def H(response):
    """Measure the randomness of a PUF for response """
    bit_sum = 0
    Nr = len(response)
    for i in range(Nr):
        bit_sum += response[i]
    p = (1 / Nr) * bit_sum
    return p, -log2(max(p, 1 - p))



def U(k, Ri):
    """Measure the Uniqueness of a PUF for challenge c among k chips between response set Ri and Rj"""
    uk = 0
    for i in range(k - 1):
        for j in range(i + 1):
            uk += (hammingDistance(Ri[i], Ri[j]))
    return uk * (2 / (k * (k - 1)))


def MU(Uk):
    """Average Uniqueness for K CRPs (Uk is set of uniqueness calculated for K CRPs)"""
    mu = 0
    for i in range(1, len(Uk)):
        mu += Uk[i]
    return mu * (1 / len(Uk))


# def R(Ri, Ri_):
#     """Reliability Between PUF response Ri and  PUF response Ri_(t), response at different conditions """
#     hd_indra = 0

#     for t in range(len(Ri_)):
#         hd_indra += (hammingDistance(Ri, Ri_[t]) / len(Ri)) * 0.01
#     hd_indra *= 1 / len(Ri_)
#     return 0.01 - hd_indra


def D(k, R):
    """Measures how different are the set of responses from the same PUF instance to different challenges"""
    norma = 4/k**2
    sum_ele = 0
    for i in range(k-1):
        for j in range(i+1, k):
            sum_ele += R[i] ^ R[j]

    return norma * sum_ele
