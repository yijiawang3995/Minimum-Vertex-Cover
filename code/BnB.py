import operator
import time
import math



def solution(G, T):
    start_time = time.time()
    sol_trace = []  # record every new improved solution as list of (time stamp, vertex cover)

    # Initialization
    OptVC = []
    CurVC = []
    F = []

    # Initial upper bound
    UpperBound = G.number_of_nodes()

    G_prime = G.copy()
    # Sort based on degree to find the node with highest degree
    v = sort_degree(G_prime)

    # Append the node with highest degree
    # the most promising node to be included in the VC
    F.append((v[0], 0, (-1, -1)))  # node, state,(parent node, parent node state)
    F.append((v[0], 1, (-1, -1)))

    while F != [] and (time.time() - start_time) < T:
        (vi, state, parent) = F.pop()  # set current node to last element in F

        backtrack = False

        if state == 0:  # if the vertex vi does not belong to VC
            for neighbor in list(G_prime.neighbors(vi)):
                CurVC.append((neighbor, 1))  # include neighbors in VC
                G_prime.remove_node(neighbor)  # remove neighbors from G_prime
        elif state == 1:  # if the vertex vi belongs to VC
            G_prime.remove_node(vi)  # remove node from G_prime
        else:
            pass

        CurVC.append((vi, state))
        C_prime_size = VC_Size(CurVC)

        if G_prime.number_of_edges() == 0:  # all explored
            if C_prime_size < UpperBound:
                OptVC = CurVC.copy()
                # print('Current Opt VC size', C_prime_size)
                UpperBound = C_prime_size
                sol_trace.append((time.time() - start_time, C_prime_size))
            backtrack = True

        else:  # partial solution
            CurLB = Lowerbound(G_prime) + C_prime_size

            if CurLB < UpperBound:
                # Branch
                vj = sort_degree(G_prime)
                F.append((vj[0], 0, (vi, state)))  # vi is parent of vj
                F.append((vj[0], 1, (vi, state)))
            else:
                # Prune
                backtrack = True

        if backtrack == True:
            if F:
                parent = F[-1][2]  # parent of last element in F

                if parent in CurVC:
                    id = CurVC.index(parent) + 1
                    while id < len(CurVC):
                        mynode, mystate = CurVC.pop()
                        G_prime.add_node(mynode)  # add back the node to G_prime

                        CurVC_nodes = list(map(lambda v: v[0], CurVC))
                        for neigh in G.neighbors(mynode):
                            if (neigh in G_prime.nodes()) and (neigh not in CurVC_nodes):
                                G_prime.add_edge(neigh, mynode)  # add back deleted edges of vi to G_prime

                elif parent == (-1, -1):  # Root node
                    CurVC.clear()
                    G_prime = G.copy()

                else:
                    print('Error: Fail to Backtrack!')

    return OptVC, sol_trace


# Sort the vertices based on degree
def sort_degree(g):
    deg_dict = dict(g.degree())
    deg_sorted = sorted(deg_dict.items(), reverse=True, key=operator.itemgetter(1))
    return deg_sorted[0]


# Compute lower bound for G_prime
def Lowerbound(graph):
    return math.ceil(graph.number_of_edges() / sort_degree(graph)[1])


# Compute size of vertex cover
def VC_Size(VC):
    ct = 0
    for v in VC:
        ct = ct + v[1]
    return ct

