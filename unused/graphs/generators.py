import networkx as nx
import random


def generate_random_graph(n=30, k=8, p=0.25, weight_range=(1, 10), seed=None, directed=True):
    if seed is not None:
        random.seed(seed)

    undirected = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=seed)

    if directed:
        g = nx.DiGraph()
    else:
        g = nx.Graph()

    for u, v in undirected.edges():
        if directed:
            if random.random() < 0.5:
                src, tgt = u, v
            else:
                src, tgt = v, u
            weight = random.randint(*weight_range)
            g.add_edge(src, tgt, weight=weight)

            # sieje ferment
            if random.random() < 0.2:
                weight2 = random.randint(*weight_range)
                g.add_edge(tgt, src, weight=weight2)
        else:
            weight = random.randint(*weight_range)
            g.add_edge(u, v, weight=weight)

    return g


