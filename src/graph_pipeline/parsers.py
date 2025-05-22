import ast
import networkx as nx
from .core import GraphWrapper
from pathlib import Path


def parse_edge_list(path: Path, graph_family: str = None) -> GraphWrapper:
    Gnx = nx.read_weighted_edgelist(path, nodetype=int)
    nodes = list(Gnx.nodes())
    edges = [(u, v, data.get('weight', 1))
             for u, v, data in Gnx.edges(data=True)
    ]

    directed = Gnx.is_directed()
    fam = graph_family or _infer_family(Gnx)
    return GraphWrapper(nodes, edges,
                        directed=directed,
                        graph_family=fam,
                        original_filename=path.name)


def parse_dict_edgelist(path: Path, graph_family: str = None) -> GraphWrapper:
    Gnx = nx.DiGraph()
    nodes_set = set()

    with path.open() as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            u, v, raw = line.split(maxsplit=2)
            weight = ast.literal_eval(raw).get("weight", 1.0)
            u, v = int(u), int(v)
            Gnx.add_edge(u, v, weight=weight)
            nodes_set.update({u, v})

    nodes = list(nodes_set)
    fam = graph_family or _infer_family(Gnx)
    edges = [(u, v, data.get('weight', 1.0))
             for u, v, data in Gnx.edges(data=True)]

    return GraphWrapper(nodes, edges,
                        directed=True,
                        graph_family=fam,
                        original_filename=path.name)


def parse_adj_matrix(path: Path, graph_family: str = None) -> GraphWrapper:
    import numpy as np
    mat = np.loadtxt(path)
    n = mat.shape[0]
    edges = [(i, j, mat[i, j])
             for i in range(n)
             for j in range(n)
             if mat[i, j] != 0]

    Gnx = nx.DiGraph() if False else nx.Graph()
    family = graph_family or ("bipartite" if nx.is_bipartite(Gnx.edges) else "unknown")
    return GraphWrapper(list(range(n)), edges,
                        directed=False,
                        graph_family=family,
                        original_filename=path.name)


def infer_and_parse(path: Path, graph_family: str = None) -> GraphWrapper:
    ext = path.suffix.lower()
    if ext in {".edgelist", ".txt"}:
        return parse_edge_list(path, graph_family)
    if ext == ".dictedgelist":
        return parse_dict_edgelist(path, graph_family)
    if ext in {".mtx", ".csv"}:
        return parse_adj_matrix(path, graph_family)
    raise ValueError(f"unsupported graph format: {ext}")


def _infer_family(Gnx: nx.Graph) -> str:
    if Gnx.is_directed():
        return "directed"
    if nx.is_bipartite(Gnx):
        return "bipartite"
    try:
        if nx.is_connected(Gnx) and nx.check_planarity(Gnx)[0]:
            return "planar"
    except Exception:
        pass
    return "unknown"
