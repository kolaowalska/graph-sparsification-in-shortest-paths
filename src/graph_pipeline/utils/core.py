import networkx as nx


class GraphWrapper:
    def __init__(self, nodes, edges, directed=False, graph_family="unknown", original_filename="unknown"):
        self.is_directed = directed
        self.G = nx.DiGraph() if directed else nx.Graph()
        self.G.add_nodes_from(nodes)
        for u, v, w in edges:
            if isinstance(w, dict):
                self.G.add_edge(u, v, **w)
            else:
                self.G.add_edge(u, v, weight=w)
        self.graph_family = graph_family
        self.original_filename = original_filename

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

    def __repr__(self):
        return(f"GraphWrapper (n={self.n}, m={self.m}, directed={self.is_directed}, "
               f"family='{self.graph_family}', file='{self.original_filename}')")
