# File containing an implementation of the FastVC algorithm.

from datetime import datetime, timedelta
from random import choice, seed, random
from itertools import chain


# Read an input graph into a sparse adjacency matrix line by line without reading in the isolate vertexes
def read_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        file.readline()
        for i, line in enumerate(file):
            if len(line.strip()) > 0:
                graph[i] = set(int(i) - 1 for i in line.split())
    return graph


# Gets all of the edges in a graph without duplicates or reversed edges
def get_edges(graph):
    return list(set(chain(
        *[[(u, v) if u < v else (v, u) for v in graph[u]] for u in graph]
    )))


# Check whether the solution is a valid solution to MVC problem
def is_solution(graph, vc):
    # Each edge has at least one endpoint in the vertex cover
    for u in graph:
        for v in graph[u]:
            if vc[u] + vc[v] == 0:
                return False
    return True


# Remove a vertex to remove based on its loss value
def choose_rm_vertex(losses, vc, k=50):
    # Get all of the vertices which are currently in the VC
    indices = [i for i in range(len(vc)) if vc[i] == 1]
    best = indices[0]
    # Set k=50
    for i in range(k):
        r = choice(indices)
        if losses[r] < losses[best]:
            best = r
    return best


def random_uncovered_edge(edges, vc):
    # Keep getting random edges until one is uncovered, then return that one
    r = choice(edges)
    while vc[r[0]] + vc[r[1]] > 0:
        r = choice(edges)
    return r


# Construct a vertex cover
def construct_vc(graph):
    vc = [0] * (max(graph) + 1)
    edges = get_edges(graph)
    # entend C to cover all edges
    for u, v in edges:
        if vc[u] + vc[v] == 0:
            vc[max(u, v, key=lambda x: len(graph[x]))] = 1

    # Compute the loss for each vertex in the graph, updates neighbors' loss
    losses = [0] * len(vc)
    for u, v in edges:
        if vc[u] + vc[v] == 1:
            if vc[u] > vc[v]:
                losses[u] += 1
            else:
                losses[v] += 1

    # Remove vertices that have zero loss, update the loss of its neighbors
    for u in range(len(vc)):
        if losses[u] == 0:
            # worsen the initial cover
            if random()<0.7:
                vc[u] = 0
                if u in graph:
                    for v in graph[u]:
                        losses[v] += 1

    return vc, losses


def fast_vc(graph, filename, cutoff_time, random_seed):
    seed(random_seed)

    # Basic setup
    i=0
    vc, losses = construct_vc(graph)
    gains = [0] * len(vc)
    edges = get_edges(graph)
    best = None
    sol_trace = []

    start_time = now_time = datetime.now()
    inf = float('inf')

    while now_time - start_time < timedelta(seconds=cutoff_time) and i<2000:
        if is_solution(graph, vc):
            best = [i for i in vc]
            i=0
            sol_trace.append(((now_time - start_time).total_seconds(), sum(best)))

            # Find the vertex with minimum loss and remove it
            min_loss = min([i for i in range(len(vc))],
                           key=lambda i: inf if vc[i] == 0 else losses[i])
            vc[min_loss] = 0

            # Gains is 0 now for the vertex because it is in the VC
            gains[min_loss] = 0

            # Update the losses and gains of all neighbors to the min loss
            # vertex; they should all increase because edges will now
            # potentially be uncovered
            for v in graph[min_loss]:
                if vc[v] == 0:
                    gains[v] += 1
                else:
                    losses[v] += 1
            continue

        # Remove the vertex with approximately minimum loss
        u = choose_rm_vertex(losses, vc)
        vc[u] = 0
        gains[u] = 0

        # update the losses and gains of surrounding vertices accordingly
        for v in graph[u]:
            if vc[v] == 0:
                gains[v] += 1
            else:
                losses[v] += 1

        # find a random uncovered edge
        e0, e1 = random_uncovered_edge(edges, vc)

        # add its endpoint with greater gain to the VC
        u = max(e0, e1, key=lambda x: gains[x])
        vc[u] = 1

        # update losses and gains of vertices in VC
        for v in graph[u]:
            if vc[v] == 0:
                gains[v] -= 1
            else:
                losses[v] -= 1
        now_time = datetime.now()
        if len(vc) == len(best):
                i += 1

    vc = [str(i + 1) for i in range(len(best)) if best[i] == 1]
    return vc, sol_trace


def run(filename, cutoff_time, random_seed):
    seed(random_seed)
    graph = read_graph(filename)
    return fast_vc(graph, filename, cutoff_time, random_seed)
