import networkx as nx
from collections import Counter


def degree_distribution(G: nx.Graph) -> dict:
    n = G.number_of_nodes()

    if n == 0:
        return {}

    if not isinstance(G, nx.DiGraph):
        deg_counts = Counter(dict(G.degree()).values())
        return {deg: cnt / n for deg, cnt in deg_counts.items()}

    '''
    AAAAAAAAAAAA CZEMU TO NIE DZIALAAA TESKNIE ZA C++
    in_counts = Counter(dict(G.in_degree()).values())
    out_counts = Counter(dict(G.out_degree()).values())
    '''

    if G.is_directed():
        in_deg = Counter()
        out_deg = Counter()
        for u, v in G.edges():
            out_deg[u] += 1
            in_deg[v] += 1
        for v in G.nodes():
            in_deg.setdefault(v, 0)
            out_deg.setdefault(v, 0)

        indegree_distribution = {d: c / n for d, c in Counter(in_deg.values()).items()}
        outdegree_distribution = {d: c / n for d, c in Counter(out_deg.values()).items()}

        return {'indegree_distribution': indegree_distribution,
                'outdegree_distribution' : outdegree_distribution}

    deg = Counter()
    for u, v in G.edges():
        deg[u] += 1
        deg[v] += 1
    for v in G.nodes():
        deg.setdefault(v, 0)

    return {d: c / n for d, c in Counter(deg.values()).items()}


def is_connected(G: nx.Graph) -> bool:
    if G.is_directed():
        return nx.is_weakly_connected(G)
    return nx.is_connected(G)

