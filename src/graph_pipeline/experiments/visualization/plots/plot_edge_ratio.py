import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# edge ratio by sparsifier method and graph family
def plot_edge_ratio(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['edges_ratio', 'method', 'graph_family']):
        print("skipping 'edge ratio' plot: required columns are missing")
        return

    plt.figure(figsize=(14, 8)) #
    sns.boxplot(data=df, x='method', y='edges_ratio', hue='graph_family', palette='viridis')
    plt.title('edge ratio by sparsifier method and graph family', fontsize=16)
    plt.ylabel('edges ratio (m_sparse / m_og)', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='graph family', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    plot_filename = plots_dir / 'edges_ratio_by_method_family.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.show()
    plt.close()
