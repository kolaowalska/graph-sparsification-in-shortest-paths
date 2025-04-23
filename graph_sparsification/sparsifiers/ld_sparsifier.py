import networkx as nx
import math


def local_degree_sparsifier(
        G: nx.DiGraph,
        alpha: float = 0.5) -> nx.DiGraph:
    """
    :param G: directed graph with edge weights as 'weight'
    :param alpha: edge retention parameter
    :return: H (nx.DiGraph) - sparsified subgraph
    """

    assert 0 <= alpha <= 1

    H = nx.DiGraph()
    H.add_nodes_from(G.nodes(data=True))

    for v in G.nodes():
        out_edges = list(G.out_edges(v, data=True))
        d_out = len(out_edges)
        if d_out == 0:
            continue

        # number of neighbors to retain
        k = max(1, math.floor(d_out ** alpha))

        # ranking the outgoing edges by the out-degree of their target node
        ranked_edges = sorted(
            out_edges,
            key=lambda e: G.out_degree[e[1]], # zaraz oszaleje czemu to nie dziala
            reverse=True
        )

        for u, w, data in ranked_edges[:k]:
            H.add_edge(u, w, **data)

    return H
