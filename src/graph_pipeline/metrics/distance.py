import networkx as nx
import math
from typing import Any, Dict, Optional, Union


def apsp_matrix(
        G_input: Union[nx.Graph, object],
        weight: Optional[str] = 'weight'
) -> Dict[Any, Dict[Any, float]]:
    """
    computes all-pairs shortest-path distances for a given graph G
    if weight is None uses unweighted BFS (edge length = 1),
    otherwise just uses johnson with positive weights falling back to floyd-warshall

    returns dist[u][v] = float distance of math.inf if unreachable
    """
    G = getattr(G_input, 'G', getattr(G_input, '_G', G_input))
    # print(list(G.nodes()))
    if weight is None:
        raw = dict(nx.all_pairs_shortest_path_length(G))
    else:
        try:
            raw = dict(nx.johnson(G, weight=weight))
        except Exception:
            raw = dict(nx.floyd_warshall(G, weight=weight))

    nodes = list(G.nodes())
    dist: Dict[Any, Dict[Any, float]] = {u: {v: math.inf for v in nodes} for u in nodes}

    for u, row in raw.items():
        dist[u][u] = 0.0
        for v, d in row.items():
            if isinstance(d, list):
                value = float(len(d) - 1)
            else:
                try:
                    value = float(d)
                except Exception:
                    value = math.inf
            dist[u][v] = value
    return dist


def graph_diameter(
        dist: Dict[Any, Dict[Any, float]]
) -> float:
    all_vals = [d for row in dist.values() for d in row.values()]
    if any(math.isinf(d) for d in all_vals if d is not None):
        return math.inf
    return max(all_vals) if all_vals else 0.0


def unreachable_pairs_ratio(
        dist: Dict[Any, Dict[Any, float]],
        n: int
) -> float:
    if n <= 1:
        return 0.0
    total = n * (n - 1)
    unreachable = sum(
        1 for u in dist for v in dist[u]
        if u != v and math.isinf(dist[u][v])
    )
    return unreachable / total


def local_stretch(
        G_dist: Dict[Any, Dict[Any, float]],
        H_dist: Dict[Any, Dict[Any, float]]
) -> Dict[Any, float]:
    stretch: Dict[Any, float] = {}
    for u, row in G_dist.items():
        for v, dG in row.items():
            if u != v and dG > 0 and not math.isinf(dG):
                dH = H_dist.get(u, {}).get(v, math.inf)
                stretch[(u, v)] = dH / dG
    return stretch


def stretch_avg(stretch: Dict[Any, float]) -> float:
    values = [s for s in stretch.values() if not math.isinf(s)]
    return sum(values) / len(values) if values else math.inf


def stretch_var(stretch: Dict[Any, float]) -> float:
    values = [s for s in stretch.values() if not math.isinf(s)]
    if len(values) < 2:
        return 0.0 if values else math.inf
    mean = sum(values) / len(values)
    return sum((x - mean)**2 for x in values) / len(values)


def max_stretch(stretch: Dict[Any, float]) -> float:
    values = [s for s in stretch.values() if not math.isinf(s)]
    return max(values) if values else math.inf
