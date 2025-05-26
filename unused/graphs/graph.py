import networkx as nx


class Graph:
    def __init__(self, directed: bool = False, weighted: bool = False):
        self.directed = directed
        self.weighted = weighted
        self._G = nx.DiGraph() if directed else nx.Graph()

    @classmethod
    def from_nx(cls, G: nx.Graph):
        wrapper = cls(directed=G.is_directed(),
                      weighted='weight' in nx.get_edge_attributes(G, 'weight'))
        wrapper._G = G.copy()
        return wrapper

    def add_edge(self, u, v, weight: float = 1.0):
        if self.weighted:
            self._G.add_edge(u, v, weight=weight)
        else:
            self._G.add_edge(u, v)

    def is_weighted(self, attr: str = 'weight') -> bool:
        return any(attr in data for _, _, data in self._G.edges(data=True))

    @property
    def nodes(self):
        return self._G.nodes

    @property
    def edges(self):
        return self._G.edges(data=True)

    @property
    def number_of_nodes(self):
        return self._G.number_of_nodes()

    @property
    def number_of_edges(self):
        return self._G.number_of_edges()

    @property
    def is_directed(self):
        return self._G.is_directed()

    @property
    def G(self):
        return self._G

