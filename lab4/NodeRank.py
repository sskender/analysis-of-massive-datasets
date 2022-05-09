import sys


N = 0
beta = 0
max_iteration = 0
outgoing_nodes = []
ingoing_nodes = []
iter_node_ranks_matrix = {}


def calc_rank(r_iteration, r_node_idx):
    """ Request iteration n  and request node index """
    global max_iteration

    for iteration_i in range(max_iteration + 1, r_iteration + 1):
        for node_idx in range(N):
            sum_ri_di = 0
            previous_iteration = iteration_i - 1
            for ingoing_node_idx in ingoing_nodes[node_idx]:
                ri = iter_node_ranks_matrix[(previous_iteration, ingoing_node_idx)]
                di = len(outgoing_nodes[ingoing_node_idx])
                sum_ri_di += ri / di
            rj = beta * sum_ri_di + (1 - beta) / N
            iter_node_ranks_matrix[(iteration_i, node_idx)] = rj

    if r_iteration > max_iteration:
        max_iteration = r_iteration

    return iter_node_ranks_matrix[(r_iteration, r_node_idx)]


def main():
    """ Load and execute """
    global N
    global beta
    n_str, beta_str = sys.stdin.readline().split()
    N = int(n_str)
    beta = float(beta_str)

    # load nodes and edges
    for _ in range(N):
        ingoing_nodes.append([])
    for node_idx in range(N):
        edges_list = list(map(int, sys.stdin.readline().split()))
        outgoing_nodes.append(edges_list)
        for edge_idx in edges_list:
            if node_idx not in ingoing_nodes[edge_idx]:
                ingoing_nodes[edge_idx].append(node_idx)

    # calculate iteration 0
    iteration_0 = 0
    for node_idx in range(N):
        iter_node_ranks_matrix[(iteration_0, node_idx)] = 1 / N

    # execute queries
    Q = int(sys.stdin.readline())
    for _ in range(Q):
        node_idx, iteration = list(map(int, sys.stdin.readline().split()))
        rank = calc_rank(iteration, node_idx)
        print("%.10f" % rank)


if __name__ == "__main__":
    main()
