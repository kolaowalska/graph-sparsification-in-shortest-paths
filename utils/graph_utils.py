import networkx as nx


def symmetrize_graph(D: nx.DiGraph,
                     weight: str = 'weight',
                     mode: str = 'min') -> nx.Graph:
    """
    converts a directed graph D into an undirected graph G by merging
    each pair of opposite edges into a single undirected edge
    :param D: connected graph
    :param weight: name of the edge‐attribute holding the weight
    :param mode: how to combine weights when both (u,v) and (v,u) exist;
                 one of {'min','max','sum','avg'}
    :return: undirected graph G (nx.Graph) with merged weights
    """

    if not D.is_directed():
        raise ValueError("bomba bomba bomba graf jest nieskierowany")

    G = nx.Graph()
    G.add_nodes_from(D.nodes(data=True))

    for u, v, data in D.edges(data=True):
        w = data.get(weight, 1)
        if G.has_edge(u, v):
            old = G[u][v].get(weight, 1)
            if mode == 'min': new = min(old, w)
            elif mode == 'max': new = max(old, w)
            elif mode == 'sum': new = old + w
            elif mode == 'avg': new = (old + w)/2
            else:
                raise ValueError("unknown mode - get lost!!!!!!!!")
            G[u][v][weight] = new
        else:
            G.add_edge(u, v, **{weight: w})

    return G
