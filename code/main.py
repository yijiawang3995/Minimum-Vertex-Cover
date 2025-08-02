import time
import os
import argparse
import random
import networkx as nx

import BnB
import SA
import approx
import fastvc

opt_cutoff = {'karate': 14, 'football': 94, 'jazz': 158, 'email': 594, 'delaunay_n10': 703, 'netscience': 899,
              'power': 2203, 'as-22july06': 3303, 'hep-th': 3926, 'star2': 4542, 'star': 6902}


def parse_edges(filename):
    # parse edges from graph file to create your graph object
    # filename: string of the filename
    f = open(filename, "r")
    n_vertices, n_edges, _ = f.readline().split(' ')
    n_vertices, n_edges = int(n_vertices), int(n_edges)

    G = nx.Graph()  # create a graph

    for i in range(1, n_vertices + 1):
        G.add_node(i)
    # add edges to the graph
    for i in range(1, n_vertices + 1):
        neighbors = f.readline().rstrip().split(' ')
        for neighbor in neighbors:
            if neighbor != '':
                if int(neighbor) > i:
                    G.add_edge(i, int(neighbor))


    return G


def main(graph, algo, cutoff, seed):
    random.seed(seed)
    algo = algo.upper()

    graph_name = graph.split('/')[-1].split('.')[0]

    # skip dummy graph
    if graph_name not in opt_cutoff:
        return

    sol_file = "_".join([graph_name, algo, str(cutoff), str(seed)]) + '.sol'
    trace_file = "_".join([graph_name, algo, str(cutoff), str(seed)]) + '.trace'
    output_dir = './output/'  # './{}_output/'.format(algo)
    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    G = parse_edges(graph)
    start_time = time.time()

    if algo == 'BNB':
        vc_1, sol_trace = BnB.solution(G, cutoff)
        vc = [x[0] for x in vc_1]
        num_vc_nodes = len(vc)
        total_time = round((time.time() - start_time), 5)
        print('BnB Algo Runtime: ' + str(total_time))

        sol_file = "_".join([graph_name, algo, str(cutoff)]) + '.sol'
        trace_file = "_".join([graph_name, algo, str(cutoff)]) + '.trace'

    if algo == 'SA':
        S_init, C, sol_trace = SA.initial_S(G, start_time, cutoff)
        vc, num_vc_nodes, sol_trace = SA.simulate_annealing(G, S_init, C,
                                                            cutoff, start_time, sol_trace)
        total_time = round((time.time() - start_time), 5)
        print('SA Runtime (s): {}'.format(total_time))

    if algo == 'APPROX':
        num_vc_nodes, vc = approx.solution(G, start_time, cutoff, seed)
        total_time = round((time.time() - start_time), 5)
        sol_trace = [(total_time, num_vc_nodes)]
        print('Approx Algo Runtime: ' + str(total_time))

    if algo == 'FASTVC':
        vc, sol_trace = fastvc.run(graph, cutoff, seed)
        total_time = round((time.time() - start_time), 5)
        num_vc_nodes = len(vc)
        print('Fastvc Algo Runtime: ' + str(total_time))

    with open(os.path.join(output_dir, sol_file), 'w') as f:
        f.write(str(num_vc_nodes) + "\n")
        f.write(','.join([str(n) for n in sorted(vc)]))

    with open(os.path.join(output_dir, trace_file), 'w') as f:
        for t in sol_trace:
            f.write(str(t[0]) + ',' + str(t[1]) + '\n')


# Run as executable from terminal
if __name__ == '__main__':
    # parse arguments in the following format:

    parser = argparse.ArgumentParser(
        description='Run algorithm with specified parameters')
    parser.add_argument('-inst', type=str, required=True, help='graph file')
    parser.add_argument('-alg', type=str, required=True,
                        help='algorithm to use')
    parser.add_argument('-time', type=float, default=100,
                        required=False, help='runtime cutoff for algorithm')
    parser.add_argument('-seed', type=int, default=30,
                        required=False, help='random seed for algorithm')
    args = parser.parse_args()

    main(args.inst, args.alg, args.time, args.seed)
