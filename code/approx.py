import random
import sys
import networkx as nx
import time

sys.setrecursionlimit(1000000)


def solution(G, start_time, cutoff_time, seed):
    def increase(node):
        node += 1
        if node > num_vertex:
            node = node % num_vertex
        return node

    def dfs(node):
        visited.add(node)
        if G.has_node(node):
            for neighbor in list(G[node]):
                if neighbor not in visited:
                    non_leaf.add(node)
                    dfs(neighbor)


    visited = set()
    non_leaf = set()
    num_vertex = G.number_of_nodes()

    random.seed(seed)
    end_node = 0
    if seed != -1:
        end_node = random.randint(1, num_vertex)

    cur_node = increase(end_node)

    while cur_node != end_node:
        if time.time() - start_time > cutoff_time:
            return 0, []
        if cur_node not in visited:
            dfs(cur_node)
        cur_node = increase(cur_node)
    dfs(end_node)

    return len(non_leaf), list(non_leaf)




