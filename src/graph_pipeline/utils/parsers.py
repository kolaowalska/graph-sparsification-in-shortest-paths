import ast
import networkx as nx
import numpy as np
from utils.core import GraphWrapper
from pathlib import Path


def parse_edgelist(path: Path, graph_family: str = None) -> GraphWrapper:
    Gnx = nx.read_weighted_edgelist(path, nodetype=int, create_using=nx.DiGraph())
    directed = not nx.is_directed_acyclic_graph(Gnx.to_undirected(as_view=True))

    if not directed:
        Gnx = Gnx.to_undirected()

    family = graph_family or _infer_family(Gnx)

    if family == 'undirected' or family == "bipartite":
        directed = False

    nodes = list(Gnx.nodes())
    edges = [
        (u, v, data.get('weight', 1))
        for u, v, data in Gnx.edges(data=True)
    ]

    return GraphWrapper(nodes, edges,
                        directed=directed,
                        graph_family=family,
                        original_filename=path.name)


def parse_dict_edgelist(path: Path, graph_family: str = None) -> GraphWrapper:
    Gnx = nx.DiGraph()

    with path.open() as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            u, v, raw = line.split(maxsplit=2)
            u, v = int(u), int(v)
            weight = ast.literal_eval(raw).get("weight", 1.0)
            Gnx.add_edge(u, v, weight=weight)

    directed = not nx.is_directed_acyclic_graph(Gnx.to_undirected(as_view=True))

    if not directed:
        Gnx = Gnx.to_undirected()

    family = graph_family or _infer_family(Gnx)
    nodes = list(Gnx.nodes())
    edges = [
        (u, v, data.get('weight', 1.0))
        for u, v, data in Gnx.edges(data=True)
    ]

    return GraphWrapper(nodes, edges,
                        directed=directed,
                        graph_family=family,
                        original_filename=path.name)


def parse_adj_matrix(path: Path, graph_family: str = None) -> GraphWrapper:
    mat = np.loadtxt(path)
    n = mat.shape[0]

    directed = not np.allclose(mat, mat.T, atol=1e-10)
    edges = [
        (i, j, mat[i, j])
        for i in range(n)
        for j in range(n)
        if mat[i, j] != 0
    ]

    Gnx = nx.DiGraph() if directed else nx.Graph()
    Gnx.add_weighted_edges_from(edges)
    family = graph_family or _infer_family(Gnx)

    return GraphWrapper(list(range(n)), edges,
                        directed=directed,
                        graph_family=family,
                        original_filename=path.name)


def infer_and_parse(path: Path, graph_family: str = None) -> GraphWrapper:
    ext = path.suffix.lower()
    if ext in {".edgelist", ".txt"}:
        return parse_edgelist(path, graph_family)
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
