import networkx as nx
import math
import numbers
from typing import Any, Dict, Optional


def apsp_matrix(G: nx.Graph, weight: Optional[str] = 'weight') -> Dict[Any, Dict[Any, float]]:
    """
    computes all-pairs shortest-path distances for a given graph G
    if weight is None uses unweighted BFS (edge length = 1), otherwise uses johnson with positive weights falling back to floyd-warshall

    returns dist[u][v] = float distance of math.inf if unreachable
    if the returned value is a path list, its length - 1 is used
    """
    nodes = list(G.nodes())
    # getting raw distances
    if weight is None:
        raw_iter = nx.all_pairs_shortest_path_length(G)
    else:
        try:
            raw_iter = nx.johnson(G, weight=weight).items()
        except nx.NetworkXError:
            raw_iter = nx.floyd_warshall(G, weight=weight).items()

    dist: Dict[Any, Dict[Any, float]] = {}
    for u, row in raw_iter:
        inner: Dict[Any, float] = {}
        for v, d in row.items():
            if isinstance(d, list):
                # rows from dfs might return full paths
                inner[v] = float(len(d) - 1)
            elif isinstance(d, numbers.Number):
                inner[v] = float(d)
            else:
                try:
                    inner[v] = float(d)
                except Exception:
                    raise TypeError(f"jezeli bog stworzyl czlowieka a czlowiek maszyne "
                                    f"to jedyne co pozostaje ludzkosci to blagac o przebaczenie")
        # enforcing self-distance
        inner[u] = 0.0
        for v in nodes:
            if v not in inner:
                inner[v] = math.inf
        dist[u] = inner

    for u in nodes:
        if u not in dist:
            dist[u] = {v: (0.0 if v == u else math.inf) for v in nodes}

    return dist


def graph_diameter(dist: Dict[Any, Dict[Any, float]]) -> float:
    n = len(dist)
    if unreachable_pairs_ratio(dist, n) > 0:
        return math.inf
    finite = [d for row in dist.values() for d in row.values() if not math.isinf(d)]
    if not finite:
        return 0.0
    return max(finite)


def unreachable_pairs_ratio(dist: Dict[Any, Dict[Any, float]], n: int) -> float:
    if n <= 1:
        return 0.0
    total = n * (n - 1)
    unreachable = 0
    for u, row in dist.items():
        for v, d in row.items():
            if u != v and math.isinf(d):
                unreachable += 1
    return unreachable / total


def local_stretch(G_dist: Dict[Any, Dict[Any, float]],
                  H_dist: Dict[Any, Dict[Any, float]]) -> Dict[Any, float]:
    stretch: Dict[Any, float] = {}
    for u, rowG in G_dist.items():
        for v, dG in rowG.items():
            if u == v or math.isinf(dG):
                continue
            dH = H_dist.get(u, {}).get(v, math.inf)
            stretch[(u, v)] = dH / dG if dH < math.inf else math.inf
    return stretch


def stretch_avg(stretch: Dict[Any, float]) -> float:
    finite = [s for s in stretch.values() if not math.isinf(s)]
    if not finite:
        return math.inf
    return sum(finite) / len(finite)


def stretch_var(stretch: Dict[Any, float]) -> float:
    finite = [s for s in stretch.values() if not math.isinf(s)]
    n = len(finite)
    if n == 0:
        return math.inf
    if n == 1:
        return 0.0
    mean = sum(finite) / n
    return sum((x - mean) ** 2 for x in finite) / n


def max_stretch(stretch: Dict[Any, float]) -> float:
    finite = [s for s in stretch.values() if not math.isinf(s)]
    if not finite:
        return math.inf
    return max(finite)
