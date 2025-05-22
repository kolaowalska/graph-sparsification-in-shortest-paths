import ast
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
        if nx.is_connected(Gnx) and nx.check_planarity(Gnx)[0]:
            graph_family = "planar"
    except Exception:
        pass

    return GraphWrapper(
        nodes,
        edges,
        directed=is_directed,
        graph_family=graph_family,
        original_filename=path.name
    )


def parse_dict_edgelist(path: pathlib.Path) -> GraphWrapper:
    Gnx = nx.DiGraph()
    nodes_set = set()

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(maxsplit=2)
            if len(parts) < 3:
                print(f"warning: skipping malformed line {line} in {path.name}")
                continue

            try:
                u = int(parts[0])
                v = int(parts[1])
                weight_dict_str = parts[2]
                weight_dict = ast.literal_eval(weight_dict_str)
                weight = weight_dict.get('weight', 1.0)

                Gnx.add_edge(u, v, weight=weight)
                nodes_set.add(u)
                nodes_set.add(v)

            except (ValueError, SyntaxError, TypeError) as e:
                print(f"error parsing line {line} in {path.name}: {e}")
                continue

    nodes = list(nodes_set)

    is_directed = Gnx.is_directed()
    graph_family = "unknown"
    if is_directed:
        graph_family = "directed"
    elif nx.is_bipartite(Gnx):
        graph_family = "bipartite"
    try:
        if nx.is_connected(Gnx) and nx.check_planarity(Gnx)[0]:
            graph_family = "planar"
    except Exception:
        pass

    edges = [(u, v, data.get('weight', 1.0)) for u, v, data in Gnx.edges(data=True)]

    return GraphWrapper(
        nodes,
        edges,
        directed=is_directed,
        graph_family=graph_family,
        original_filename=path.name
    )


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
    return GraphWrapper(list(range(n)), edges, directed=is_directed, graph_family=graph_family, original_filename=path.name)


def infer_and_parse(path: pathlib.Path) -> GraphWrapper:
    ext = path.suffix.lower()
    if ext == '.dictedgelist':
        # return parse_dict_edgelist(path)
        pass
    if ext in {'.edgelist', '.txt'}:
        return parse_edge_list(path)
    if ext in {'.mtx', '.csv'}:
        return parse_adj_matrix(path)
    raise ValueError(f"unsupported graph format: {ext}")


