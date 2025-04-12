import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import defaultdict


def kols_sparsifier(
        G: nx.DiGraph,
        k: int = 10,
        rho: float = 0.5,
        rescale: bool = True,
        seed: int = None) -> nx.DiGraph:
    """
    performs BFS-based sparsification on a directed, weighted graph G
    :param G: directed graph with edge weights as 'weight'
    :param k: number of BFS runs
    :param rho: target edge retention ratio (0 < rho <= 1)
    :param rescale: whether to rescale edge weights after sparsification
    :param seed: optional random seed
    :return: H (ns.DiGraph) - sparsified subgraph
    """

    if seed is not None:
        random.seed(seed)

    edge_freq = defaultdict(int)
    nodes = list(G.nodes)

    for _ in range(k):
        start = random.choice(nodes)
        visited = set()
        queue = [start]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            for neighbor in G.successors(current):
                edge = (current, neighbor)
                edge_freq[edge] += 1
                if neighbor not in visited:
                    queue.append(neighbor)

    # frequency normalization
    total_freq = sum(edge_freq.values())
    if total_freq == 0:
        raise ValueError("no edges traversed during bfs :(")

    frequencies = {e: f/total_freq for e, f in edge_freq.items()}

    # estimating τ as median frequency (can be user-defined)
    sorted_freqs = sorted(frequencies.values())
    tau = sorted_freqs[len(sorted_freqs) // 2] if sorted_freqs else 1e-9

    # computing retention scores (min(1, freq / τ))
    scores = {e: min(1.0, frequencies[e] / tau) for e in frequencies}

    # sorting edges by score descending and keeping top rho-fraction
    number_edges_to_keep = max(1, int(rho * G.number_of_edges()))
    top_edges = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:number_edges_to_keep]

    # computing sampling probabilities
    # probs = {e : min(1.0, (frequencies[e] / tau)) for e in frequencies}

    # builds sparsified subgraph
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes(data=True))

    for (u, v), _ in top_edges:
        original_weight = G[u][v].get("weight", 1)
        frequency = edge_freq.get((u, v), 0)
        weight = original_weight * frequency / k if rescale else original_weight
        H.add_edge(u, v, weight=weight)

    '''
    for (u, v), p in probs.items():
        if random.random() <= p:
            original_weight = G[u][v].get("weight", 1)
            frequency = edge_freq[(u, v)]

            if rescale:
                new_weight = original_weight * frequency / k
            else:
                new_weight = original_weight

            H.add_edge(u, v, weight=new_weight)
    '''

    return H


def draw_graphs(G, H, title_g="original graph G", title_h="sparsified subgraph H"):
    pos = nx.spring_layout(G, seed=42, k=1.5)  # increased k value, default is ~1/sqrt(n)
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))

    nx.draw(G, pos, with_labels=True, ax=axs[0], node_color='thistle', edge_color='gray', arrows=True)
    edge_labels_g = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_g, ax=axs[0])
    axs[0].set_title(title_g)

    node_count_g = G.number_of_nodes()
    edge_count_g = G.number_of_edges()
    axs[0].text(0.05, 0.95, f'G node count: {node_count_g}\nG edge count: {edge_count_g}',
                transform=axs[0].transAxes, fontsize=12, verticalalignment='top')

    nx.draw(H, pos, with_labels=True, ax=axs[1], node_color='lightpink', edge_color='black', arrows=True)
    edge_labels_h = nx.get_edge_attributes(H, 'weight')
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels_h, ax=axs[1])
    axs[1].set_title(title_h)

    node_count_h = H.number_of_nodes()
    edge_count_h = H.number_of_edges()
    axs[1].text(0.05, 0.95, f'H node count: {node_count_h}\nH edge count: {edge_count_h}',
                transform=axs[1].transAxes, fontsize=12, verticalalignment='top')

    plt.tight_layout()
    plt.show()


def generate_random_graph(n=30, k=5, p=0.3, weight_range=(1, 10), seed=None):

    if seed is not None:
        random.seed(seed)

    undirected = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=seed)
    g = nx.DiGraph()

    for u, v in undirected.edges():
        if random.random() < 0.5:
            src, tgt = u, v
        else:
            src, tgt = v, u

        weight = random.randint(*weight_range)
        g.add_edge(src, tgt, weight=weight)

        if random.random() < 0.2:
            weight2 = random.randint(*weight_range)
            g.add_edge(tgt, src, weight=weight2)

    return g


if __name__ == "__main__":
    G2 = nx.DiGraph()
    G2.add_weighted_edges_from([
        (0, 1, 2), (1, 2, 3), (2, 3, 4), (0, 3, 1),
        (3, 0, 2), (2, 0, 1), (1, 3, 1)
    ])

    G = generate_random_graph(n=30, k=6, p=0.3, weight_range=(1, 10), seed=42)

    H = kols_sparsifier(G, k=3, rho=0.45, rescale=True, seed=42)

    print(f"original graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"sparsified graph: {H.number_of_nodes()} nodes, {H.number_of_edges()} edges")

    draw_graphs(G, H)


