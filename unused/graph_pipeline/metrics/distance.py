import networkx as nx
import networkit as nk
import math
from typing import Any, Dict, Optional, Union, Tuple
from joblib import Parallel, delayed


# zrodlo problemu: okazuje sie ze bellman-ford i dijkstra (nawet parallel dijkstra) nie radza sobie z tak
# duzymi grafami i np O(n·(m + n log n)) robi sie za duze dla mojego 8-rdzeniowego komputerka przy n, m > 100k
def apsp_matrix(
        G: Union[nx.Graph, object],
        weight: Optional[str] = 'weight'
) -> Dict[Any, Dict[Any, float]]:

    G = getattr(G, 'G', getattr(G, '_G', G))
    nodes = list(G.nodes())

    if G.number_of_edges() > 10000:
        return exact_apsp_networkit_parallel(G, weight=weight, n_jobs=-1)

    if weight is None:
        raw = dict(nx.all_pairs_shortest_path_length(G))
    elif G.is_directed():
        try:
            raw = dict(nx.johnson(G, weight=weight))
        except Exception:
            raw = dict(nx.floyd_warshall(G, weight=weight))
    else:
        raw = dict(nx.all_pairs_dijkstra_path_length(G, weight=weight))

    dist = {u: {v: math.inf for v in nodes} for u in nodes}
    for u in nodes:
        dist[u][u] = 0.0
        if u in raw:
            for v in raw[u]:
                try:
                    dist[u][v] = float(raw[u][v])
                except Exception:
                    pass

    return dist


def exact_apsp_networkit_parallel(G: nx.Graph, weight: str = "weight", n_jobs: int = -1):
    node_list = list(G.nodes())
    node_to_id = {n: i for i, n in enumerate(node_list)}
    id_to_node = {i: n for n, i in node_to_id.items()}

    nkG = nk.graph.Graph(n=len(G.nodes()), weighted=True, directed=G.is_directed())
    for u, v, data in G.edges(data=True):
        w = data.get(weight, 1.0)
        nkG.addEdge(node_to_id[u], node_to_id[v], w)

    def single_source_apsp(i):
        dij = nk.distance.Dijkstra(nkG, i, storePaths=False)
        dij.run()
        return i, dij.getDistances()

    results = Parallel(n_jobs=n_jobs, prefer="threads")(
        delayed(single_source_apsp)(i) for i in range(nkG.numberOfNodes())
    )

    dist = {id_to_node[i]: {} for i in range(nkG.numberOfNodes())}
    for i, dvec in results:
        u = id_to_node[i]
        for j, d in enumerate(dvec):
            v = id_to_node[j]
            dist[u][v] = float(d)

    return dist


# tu w ogole cos sie bombi

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
) -> Dict[Tuple[Any, Any], float]:
    stretch: Dict[Tuple[Any, Any], float] = {}
    for u, row in G_dist.items():
        for v, dG in row.items():
            if u == v or dG <= 0 or math.isinf(dG):
                continue
            try:
                dH = H_dist[u][v]
                if not math.isinf(dH):
                    stretch[(u, v)] = dH / dG
            except KeyError:
                continue
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


'''
def apsp_matrix(
        G: Union[nx.Graph, object],
        weight: Optional[str] = 'weight'
) -> Dict[Any, Dict[Any, float]]:
    # return exact_apsp_networkit_parallel(G, weight=weight, n_jobs=-1)

    G = getattr(G, 'G', getattr(G, '_G', G))

    if weight is None:
        raw = dict(nx.all_pairs_shortest_path_length(G))
    elif G.is_directed():
        try:
            raw = dict(nx.johnson(G, weight=weight))
        except Exception:
            raw = dict(nx.floyd_warshall(G, weight=weight))
    else:
        raw = dict(nx.all_pairs_dijkstra_path_length(G, weight=weight))

    nodes = list(G.nodes())
    dist: Dict[Any, Dict[Any, float]] = {u: {v: math.inf for v in nodes} for u in nodes}

    for u, row in raw.items():
        dist[u][u] = 0.0
        for v, d in row.items():
            try:
                dist[u][v] = float(d)
            except Exception:
                dist[u][v] = math.inf

    return dist
    
    
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
'''