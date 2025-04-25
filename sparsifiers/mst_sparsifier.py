from .base import Sparsifier
from graphs.graph import Graph
import networkx as nx
from graphs.utils import symmetrize_graph


class MSTSparsifier(Sparsifier):
    def name(self) -> str:
        return "mst"

    def sparsify(self, graph: Graph) -> Graph:
        G0 = graph.G
        G = G0
        if G.is_directed():
            G = symmetrize_graph(G, weight_attr='weight', mode='avg')

        H = Graph(directed=False,
                  weighted='weight' in nx.get_edge_attributes(G, 'weight'))
        H.G.add_nodes_from(G.nodes(data=True))

        for u, v, data in nx.minimum_spanning_edges(G, data=True, weight='weight'):
            H.G.add_edge(u, v, **data)

        return H