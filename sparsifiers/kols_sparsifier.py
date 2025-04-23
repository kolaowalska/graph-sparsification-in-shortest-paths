import networkx as nx
import random
from collections import defaultdict


def kols_sparsifier(
        G: nx.DiGraph,
        k: int = 10,
        rho: float = 0.5,
        rescale: bool = True,
        seed: int = None) -> nx.DiGraph:
    """
    performs BFS-based sparsification on a directed, weighted graph G
    :param G: directed graph with edge weights as 'weight'
    :param k: number of BFS runs
    :param rho: target edge retention ratio (0 < rho <= 1)
    :param rescale: whether to rescale edge weights after sparsification
    :param seed: optional random seed
    :return: H (nx.DiGraph) - sparsified subgraph
    """

    if seed is not None:
        random.seed(seed)

    edge_freq = defaultdict(int)
    nodes = list(G.nodes)

    for _ in range(k):
        start = random.choice(nodes)
        visited = set()
        queue = [start]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            for neighbor in G.successors(current):
                edge = (current, neighbor)
                edge_freq[edge] += 1
                if neighbor not in visited:
                    queue.append(neighbor)

    # frequency normalization
    total_freq = sum(edge_freq.values())
    if total_freq == 0:
        raise ValueError("no edges traversed during bfs :(")

    frequencies = {e: f/total_freq for e, f in edge_freq.items()}

    # estimating τ as median frequency (can be user-defined)
    sorted_freqs = sorted(frequencies.values())
    tau = sorted_freqs[len(sorted_freqs) // 2] if sorted_freqs else 1e-9

    # computing retention scores (min(1, freq / τ))
    scores = {e: min(1.0, frequencies[e] / tau) for e in frequencies}

    # sorting edges by score descending and keeping top rho-fraction
    no_of_edges_to_keep = max(1, int(rho * G.number_of_edges()))
    top_edges = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:no_of_edges_to_keep]

    # computing sampling probabilities
    # probs = {e : min(1.0, (frequencies[e] / tau)) for e in frequencies}

    H = nx.DiGraph()
    H.add_nodes_from(G.nodes(data=True))

    for (u, v), _ in top_edges:
        original_weight = G[u][v].get("weight", 1)
        frequency = edge_freq.get((u, v), 0)
        if rescale:
            weight = round(original_weight * frequency / k)
        else:
            weight = original_weight
        H.add_edge(u, v, weight=weight)

    ''' old version:
    for (u, v), p in probs.items():
        if random.random() <= p:
            original_weight = G[u][v].get("weight", 1)
            frequency = edge_freq[(u, v)]

            if rescale:
                new_weight = original_weight * frequency / k
            else:
                new_weight = original_weight

            H.add_edge(u, v, weight=new_weight)
    '''

    return H
