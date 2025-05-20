import logging
import time
import networkx as nx
from typing import Dict, Any, Union, Callable, Tuple, List, Set


def symmetrize_graph(
        D: nx.DiGraph,
        weight_attr: str = 'weight',
        mode: str = 'min'
) -> nx.Graph:
    """
    converts a directed graph D into an undirected graph G by merging
    each pair of opposite edges into a single undirected edge
    :param D: connected graph
    :param weight_attr: name of the edge‐attribute holding the weight
    :param mode: how to combine weights when both (u,v) and (v,u) exist;
                 one of {'min','max','sum','avg'}
    :return: undirected graph G (nx.Graph) with merged weights
    """

    if not D.is_directed():
        return D

    G = nx.Graph()
    G.add_nodes_from(D.nodes(data=True))

    for u, v, data in D.edges(data=True):
        w = data.get(weight_attr, 1)
        if G.has_edge(u, v):
            old = G[u][v].get(weight_attr, 1)
            if mode == 'min':
                new = min(old, w)
            elif mode == 'max':
                new = max(old, w)
            elif mode == 'sum':
                new = old + w
            elif mode == 'avg':
                new = (old + w) / 2.0
            else:
                raise ValueError("unknown mode - get lost!!!!!!!!")
            G[u][v][weight_attr] = new
        else:
            G.add_edge(u, v, **{weight_attr: w})

    return G


logger = logging.getLogger("graph_pipeline")
handler = logging.FileHandler("errors.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


def timer(
        func: Callable[..., Tuple[Any, float]]
) -> Callable[..., Tuple[Any, float]]:
    def wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], (int, float)):
            return result
        return result, elapsed
    return wrapper




