import networkx as nx
from collections import Counter
from typing import Dict, Any, Union, Optional
from graphs.utils import symmetrize_graph


def degree_distribution(
        G_input: Union[nx.Graph, object]
) -> Union[Dict[int, float], Dict[str, Dict[int, float]]]:
    G = getattr(G_input, '_G', G_input)
    n = G.number_of_nodes()
    if n == 0:
        return {}

    if G.is_directed():
        in_counts = Counter(dict(G.in_degree()).values())
        out_counts = Counter(dict(G.out_degree()).values())
        return {
            'in': {d: c / n for d, c in in_counts.items()},
            'out': {d: c / n for d, c in out_counts.items()}
        }

    counts = Counter(dict(G.degree()).values())
    return {d: c / n for d, c in counts.items()}


def is_connected(G_input: Union[nx.Graph, object]) -> bool:
    G = getattr(G_input, '_G', G_input)
    if G.is_directed():
        return nx.is_weakly_connected(G)
    return nx.is_connected(G)


# L = degree matrix - adjacency matrix
# QF = x^T L x = sum_{(u,v)} w_uv (x_u - x_v)^2
def laplacian_quadratic_form(
    G_input: Union[nx.Graph, object],
    x: Optional[Dict[Any, float]] = None
) -> float:

    G = getattr(G_input, '_G', G_input)
    if G.is_directed():
        G = symmetrize_graph(G)

    nodes = list(G.nodes())
    if x is None:
        x = {v: G.degree(v, weight='weight') for v in nodes}

    qf = 0.0
    for u, v, data in G.edges(data=True):
        w = data.get('weight', 1.0)
        qf += w * (x[u] - x[v])**2

    return qf


