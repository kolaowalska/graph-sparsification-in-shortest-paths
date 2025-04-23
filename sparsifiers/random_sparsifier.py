import networkx as nx
import random


def random_sparsifier(G: nx.Graph, p: float = 0.5, seed: int = None) -> nx.Graph:
    """

    :param G: directed or undirected graph with arbitrary edge data
    :param p: probability (0 <= p <= 1) to retain each edge
    :param seed: optional random seed
    :return: sparsified subgraph H of the same type as G
    """
    assert 0 <= p <= 1

    if seed is not None:
        random.seed(seed)

    H = nx.DiGraph() if G.is_directed() else nx.Graph()
    H.add_nodes_from(G.nodes(data=True))

    for u, v, data in G.edges(data=True):
        if random.random() < p:
            H.add_edge(u, v, **data)

    return H