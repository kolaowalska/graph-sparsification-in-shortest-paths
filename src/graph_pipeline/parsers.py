import pathlib
import networkx as nx
from .core import GraphWrapper


def parse_edge_list(path: pathlib.Path) -> GraphWrapper:
    Gnx = nx.read_weighted_edgelist(path, nodetype=int)
    nodes = list(Gnx.nodes())
    edges = [(u, v, data.get('weight', 1))
             for u, v, data in Gnx.edges(data=True)
    ]

    is_directed = Gnx.is_directed()
    graph_family = "unknown"
    if is_directed:
        graph_family = "directed"
    elif nx.is_bipartite(Gnx):
        graph_family = "bipartite"
    try:
        if nx.check_planarity(Gnx)[0]:
            graph_family = "planar"
    except Exception:
        pass

    return GraphWrapper(nodes, edges, directed=is_directed, graph_family=graph_family, original_filename=path.name)


def parse_adj_matrix(path: pathlib.Path) -> GraphWrapper:
    import numpy as np
    matrix = np.loadtxt(path)
    n = matrix.shape[0]
    edges = [(i, j, matrix[i, j])
             for i in range(n)
             for j in range(n)
             if matrix[i, j] != 0
    ]

    is_directed = False
    graph_family = "unknown"
    if nx.is_bipartite(nx.Graph(edges)):
        graph_family = "bipartite"
    return GraphWrapper(list(range(n)), edges, directed=False, graph_family=graph_family, original_filename=path.name)


def infer_and_parse(path: pathlib.Path) -> GraphWrapper:
    ext = path.suffix.lower()
    if ext in {'.edgelist', '.txt'}:
        return parse_edge_list(path)
    if ext in {'.mtx', '.csv'}:
        return parse_adj_matrix(path)
    raise ValueError(f"unsupported graph format: {ext}")


