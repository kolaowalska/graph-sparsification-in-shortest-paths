import networkx as nx
import random


def k_neighbor_sparsifier(
        G: nx.DiGraph,
        k: int,
        seed: int = None) -> nx.DiGraph:
    """
    :param G: directed graph with edge weights as 'weight'
    :param k: number of outgoing edges to keep per node
    :param seed: optional random seed
    :return: H (nx.DiGraph) - sparsified subgraph
    """

    if seed is not None:
        random.seed(seed)

    H = nx.DiGraph()
    H.add_nodes_from(G.nodes(data=True))

    for v in G.nodes():
        out_edges = list(G.out_edges(v, data=True))
        deg = len(out_edges)

        if deg <= k:
            for u, w, data in out_edges:
                H.add_edge(u, w, **data)
        else:
            weights = [data.get('weight', 1) for _, _, data in out_edges]
            total_weight = sum(weights)
            probs = [w / total_weight for w in weights]

            selected_edges = random.choices(out_edges, weights=probs, k=k)

            selected = set()
            for u, w, data in selected_edges:
                if (u, w) not in selected:
                    H.add_edge(u, w, **data)
                    selected.add((u, w))

                if len(selected) >= k:
                    break

    return H