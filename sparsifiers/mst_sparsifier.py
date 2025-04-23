import networkx as nx
from utils.graph_utils import symmetrize_graph


def mst_sparsifier(G: nx.Graph) -> nx.Graph:
    """
    :param G: directed/undirected graph with edge weights as 'weight'
    :return: H (nx.DiGraph) - sparsified subgraph
    """

    if G.is_directed():
        G = symmetrize_graph(G, weight='weight', mode='min')

    H = nx.Graph()
    H.add_nodes_from(G.nodes(data=True))

    # nx’s kruskal - yields the edges of an mst in increasing‐weight order
    for u, v, data in nx.minimum_spanning_edges(G, data=True, weight='weight'):
        H.add_edge(u, v, **data)

    return H