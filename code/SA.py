#!/usr/bin/python

# Simulated Annealing (SA) is used to approximate the global optimal of the target function,
# it is proposed based on the idea of the physical process of annealing.
import time
import math
import random
import numpy as np


# create initial solution by removing the vertex won't affect the vertex cover
def initial_S(G, start_time, cutoff):
    # include all nodes
    VC = list(G.nodes())
    nV = len(VC)
    V = sorted(list(zip(list(dict(G.degree(VC)).values()), VC)), reverse=False)
    C = [0] * (nV + 1)

    i = 0
    # remove useless edges
    while (i < len(V) and (time.time() - start_time) < cutoff):
        check = True
        for x in G.neighbors(V[i][1]):
            if x not in VC:
                check = False
                break
        if check:
            # delete vertices
            VC.remove(V[i][1])
            # update cost function
            for x in G.neighbors(V[i][1]):
                C[x] += 1
        i += 1

    # print('Initial Solution:' + str(time.time()-start_time) + "," + str(len(VC)) + "\n")
    return VC, C, [(time.time() - start_time, len(VC))]


# check is vertex covered
def isVC(uncovered):
    return len(uncovered) == 0


# delete Random vertex in VC
def delRandom(S, uncovered, G, C):
    v = random.choice(S)
    S, uncovered, C = delete(S, v, uncovered, G, C)
    return S, uncovered, C

#  delete smallest cost vertex in S
def delSmallest(S, uncovered, G, C):
    #   get smallest cost
    minimum = np.inf
    for v in S:
        if C[v] < minimum:
            minimum = C[v]
            index = v
    S, uncovered, C = delete(S, index, uncovered, G, C)
    return S, uncovered, C

#  delete nodes in S and update cost function
def delete(S, v, uncovered, G, C):
    for x in G.neighbors(v):
        if x not in S:
            uncovered.append(x)
            uncovered.append(v)
    S.remove(v)
    C[v] = 0
    for x in G.neighbors(v):
        if x in S:
            C[x] += 1
    return S, uncovered, C


def add(S, u, uncovered, G, C):
    S.append(u)
    for x in G.neighbors(u):
        if x not in S:
            uncovered.remove(x)
            uncovered.remove(u)
    # update cost function
    for x in G.neighbors(u):
        if x in S:
            C[x] = C[x] - 1
        else:
            C[u] = C[u] + 1
    return S, uncovered, C


def addRandom(S, uncovered, G, C):
    u = random.choice(uncovered)
    S, uncovered, C = add(S, u, uncovered, G, C)
    return S, uncovered, C


def deltaE(Snext, S):
    E = len(S) - len(Snext)
    return E


def simulate_annealing(G, S, C, cutoff, start_time, sol_trace):
    T = 1
    uncovered = []
    i = 0
    # print(S)
    # print(str(time.time()-start_time) + "," + str(len(S)) + "\n")
    while ((time.time() - start_time) < cutoff) and (i <= (len(G) - len(S))):
        T = T * 0.9
        # looking for a better VC with less vertice
        while isVC(uncovered):
            Sret = S.copy()
            sol_trace.append((time.time() - start_time, len(Sret)))

            # delte smallest cost vertice
            S, uncovered, C = delSmallest(S, uncovered, G, C)
        S_cur = S.copy()
        uncovered_cur = uncovered.copy()
        # delete smallest cost node and add random node
        S, uncovered, C = delSmallest(S, uncovered, G, C)
        S, uncovered, C = addRandom(S, uncovered, G, C)
        # update according to simulate annealing algo
        E = deltaE(uncovered, uncovered_cur)
        if E < 0:
            p = math.exp((float(E)) / T)
            if random.uniform(0, 1) > p:
                S = S_cur.copy()
                uncovered = uncovered_cur.copy()
        if len(S) == len(S_cur):
            i += 1
    return Sret, len(Sret), sol_trace
