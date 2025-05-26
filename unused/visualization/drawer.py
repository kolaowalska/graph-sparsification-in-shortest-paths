import networkx as nx
import matplotlib.pyplot as plt


class GraphDrawer:
    @staticmethod
    def draw_graphs(
            original,
            sparsified,
            sparsifier_name: str,
            layout_seed: int = 27,
            spread_factor: float = 10.0
    ):
        G, H = original.G, sparsified.G
        position = nx.spring_layout(G, seed=layout_seed, k=spread_factor, iterations=300)
        fig, axs = plt.subplots(1, 2, figsize=(14, 7))

        nx.draw(G, position, with_labels=True, ax=axs[0], node_color='thistle', edge_color='gray', arrows=True)
        edge_labels_g = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, position, edge_labels=edge_labels_g, ax=axs[0])

        node_count_g = G.number_of_nodes()
        edge_count_g = G.number_of_edges()
        axs[0].text(0.05, 0.95, f'G node count: {node_count_g}\nG edge count: {edge_count_g}',
                    transform=axs[0].transAxes, fontsize=12, verticalalignment='top')

        nx.draw(H, position, with_labels=True, ax=axs[1], node_color='lightpink', edge_color='black', arrows=True)
        edge_labels_h = nx.get_edge_attributes(H, 'weight')
        nx.draw_networkx_edge_labels(H, position, edge_labels=edge_labels_h, ax=axs[1])

        node_count_h = H.number_of_nodes()
        edge_count_h = H.number_of_edges()
        axs[1].text(0.05, 0.95, f'H node count: {node_count_h}\nH edge count: {edge_count_h}',
                    transform=axs[1].transAxes, fontsize=12, verticalalignment='top')
        axs[1].text(0.05, 0.05, f'sparsifier: {sparsifier_name}', transform=axs[1].transAxes, fontsize=12,
                    verticalalignment='bottom', horizontalalignment='left')

        plt.tight_layout()
        plt.show()

