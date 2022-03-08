import matplotlib.pyplot as plt
import numpy as np
from base import plot_power
import pandas as pd


def LG1(num):
    A = np.ones((10,10))
    diag_elem = num - 1

    i = 0
    for row in A:
        row[i] = 0
        i += 1

    D = np.eye(num) * diag_elem

    return D - A


def LG2(num):
    shape = num
    connections = [
        [2,5,6], [1,4,5,3], [2,5,6], [2,5,7,8,11], [2,3,4,7,8,1], [1,3,7,20], [4,5,8,17,6], [4,5,7,9],
        [8,11,12,10,15], [9,11,13], [9,10,12,13,15,4,14], [9,11,13], [11,12,10,15,14], [11,13], [9,11,13,16],
        [15,17,18,19], [7,16,18,19,20], [16,17,19,20], [16,17,18], [6,17,18]
    ]

    A = np.zeros((num, num))
    i = 0
    for row in A:
        conns = connections[i]
        for num in conns:
            row[num-1] = 1
        i += 1

    D = np.zeros((shape, shape))
    j = 0

    for row in D:
        conns = connections[j]
        deg = len(conns)
        row[j] = deg
        j += 1

    return D - A


def LG3(filename):
    with open(filename, 'r') as f:
        adjM = [[int(number) for number in row.split(' ')] for row in f]


    D = np.zeros((len(adjM), len(adjM)))

    deg = []
    i = 0
    for row in adjM:
        sum = 0
        for item in row:
            sum += item
        D[i][i] = sum
        i += 1

    A = np.array(adjM)

    return D - A, adjM

def cluster(L, M):
    L3 = np.array(M)
    v, w = np.linalg.eig(L)
    idx = np.argsort(v)[::-1]
    v = v[idx]
    w = w[:, idx]
    w = w.T
    idx = np.argsort(w[-2])

    clustered = L3[np.ix_(idx, idx)]
    plt.matshow(clustered)
    plt.savefig('cluster.png', dpi=750)
    plt.show()


if __name__ == "__main__":
    LG1 = LG1(10)
    LG2 = LG2(20)
    LG3, adjM = LG3('adjacency_matrix.txt')

    # l1 = pd.DataFrame(LG1)
    # l2 = pd.DataFrame(LG2)
    # l3 = pd.DataFrame(LG3)
    # l1.to_excel('l1.xlsx', sheet_name='Sheet_1')
    # l2.to_excel('l2.xlsx', sheet_name='Sheet_1')
    # l3.to_excel('l3.xlsx', sheet_name='Sheet_1')

    L1_v, L1_w = np.linalg.eig(LG1)
    L2_v, L2_w = np.linalg.eig(LG2)
    L3_v, L3_w = np.linalg.eig(LG3)
    L1_w = L1_w[:, np.argsort(L1_v)]
    L1_w = np.flip(L1_w)
    L1_v = L1_v[np.argsort(L1_v)]
    L1_v = np.flip(L1_v)
    L2_w = L2_w[:, np.argsort(L2_v)]
    L2_w = np.flip(L2_w)
    L2_v = L2_v[np.argsort(L2_v)]
    L2_v = np.flip(L2_v)
    L3_w = L3_w[:, np.argsort(L3_v)]
    L3_w = np.flip(L3_w)
    L3_v = L3_v[np.argsort(L3_v)]
    L3_v = np.flip(L3_v)

    # L_for_plotting = [(L_1_num, 'L1'), (L_2_num, 'L2'), (L_3_num, 'L3')]
    # for L in L_for_plotting:
    #     plot_power(L[0], L[1])

    # print(L_1_vec[-2])
    # print(L_2_num)

    cluster(LG3, adjM)
