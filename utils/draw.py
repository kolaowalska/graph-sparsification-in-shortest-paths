import networkx as nx
import matplotlib.pyplot as plt


def draw_graphs(G, H, title_g="original graph G", title_h="sparsified subgraph H"):
    pos = nx.spring_layout(G, seed=93, k=1.5)  # increased k value, default is ~1/sqrt(n)
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
