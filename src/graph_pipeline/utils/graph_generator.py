from pathlib import Path
from scipy.spatial import Delaunay
import random
import networkx as nx
import numpy as np

random.seed(27)


def generate_graphs():
    base_dirs = {
        "bipartite": Path("./data/unprocessed/bipartite"),
        "directed": Path("./data/unprocessed/directed"),
        "planar": Path("./data/unprocessed/planar"),
        "unweighted": Path("./data/unprocessed/unweighted"),
        "undirected": Path("./data/unprocessed/undirected")
    }

    for dir_path in base_dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    def save_weighted_edges(graph, path):
        with open(path, "w") as f:
            for u, v, d in graph.edges(data=True):
                f.write(f"{u} {v} {d['weight']:.3f}\n")

    def save_unweighted_edges(graph, path):
        with open(path, "w") as f:
            for u, v in graph.edges():
                f.write(f"{u} {v}\n")

    def generate_planar_graph(n_points: int) -> nx.Graph:
        points = np.random.rand(n_points, 2)
        tri = Delaunay(points)
        G = nx.Graph()
        for triangle in tri.simplices:
            for i in range(3):
                u = triangle[i]
                v = triangle[(i + 1) % 3]
                G.add_edge(u, v)
        return G

    for i in range(1, 26):
        while True:
            n1 = random.randint(10, 50)
            n2 = random.randint(10, 50)
            B = nx.bipartite.random_graph(n1, n2, p=0.2)
            if nx.is_connected(B) and B.number_of_edges() <= 1000:
                break
        for u, v in B.edges():
            B[u][v]['weight'] = random.uniform(0.1, 20.0)
        save_weighted_edges(B, base_dirs["bipartite"] / f"bipartite{i}.edgelist")

    for i in range(1, 26):
        while True:
            n = random.randint(20, 100)
            G = nx.gnp_random_graph(n, p=0.1, directed=True)
            if nx.is_weakly_connected(G) and G.number_of_edges() <= 1000:
                break
        for u, v in G.edges():
            G[u][v]['weight'] = random.uniform(0.1, 20.0)
        save_weighted_edges(G, base_dirs["directed"] / f"directed{i}.edgelist")

    for i in range(1, 26):
        while True:
            n = random.randint(10, 100)
            G = generate_planar_graph(n)
            if nx.is_connected(G) and G.number_of_edges() <= 1000:
                break
        for u, v in G.edges():
            G[u][v]['weight'] = random.uniform(0.1, 20.0)
        save_weighted_edges(G, base_dirs["planar"] / f"planar{i}.edgelist")

    for i in range(1, 26):
        while True:
            n = random.randint(20, 100)
            G = nx.gnp_random_graph(n, p=0.1, directed=True)
            if nx.is_weakly_connected(G) and G.number_of_edges() <= 1000:
                break
        save_unweighted_edges(G, base_dirs["unweighted"] / f"unweighted{i}.edgelist")

    for i in range(1, 26):
        while True:
            n = random.randint(20, 100)
            G = nx.gnp_random_graph(n, p=0.1)
            if nx.is_connected(G) and G.number_of_edges() <= 1000:
                break
        for u, v in G.edges():
            G[u][v]['weight'] = random.uniform(0.1, 20.0)
        save_weighted_edges(G, base_dirs["undirected"] / f"undirected{i}.edgelist")

    print("all graphs successfully generated")


if __name__ == '__main__':
    generate_graphs()
