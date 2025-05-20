import networkx as nx


class GraphWrapper:
    def __init__(self, nodes, edges, directed=False):
        self.is_directed = directed
        self.G = nx.DiGraph() if directed else nx.Graph()
        self.G.add_nodes_from(nodes)
        for u, v, w in edges:
            if isinstance(w, dict):
                self.G.add_edge(u, v, **w)
            else:
                self.G.add_edge(u, v, weight=w)

    @property
    def nodes(self):
        return list(self.G.nodes())

    @property
    def edges(self):
        return [(u, v, data.get('weight', 1))
                for u, v, data in self.G.edges(data=True)]

    @property
    def n(self):
        return self.G.number_of_nodes()

    @property
    def m(self):
        return self.G.number_of_edges()
