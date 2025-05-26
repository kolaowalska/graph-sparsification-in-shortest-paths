import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# edge ratio by sparsifier method and graph family
def plot_edge_ratio(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['edges_ratio', 'method', 'graph_family']):
        print("skipping 'edge ratio' plot: required columns are missing")
        return

    for family in df['graph_family'].unique():
        df_family = df[df['graph_family'] == family]

        plt.figure(figsize=(10, 8))
        sns.boxplot(data=df_family, x='method', y='edges_ratio', hue='method', palette='rocket')
        plt.title(f'edge ratio by sparsification method for {family} graphs', fontsize=16)
        plt.ylabel('edges ratio (m_sparse / m_og)', fontsize=12)
        plt.xlabel('sparsification method', fontsize=12)
        plt.ylim(0, 1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend([], [], frameon=False)
        plt.tight_layout()

        plot_filename = plots_dir / f'edges_ratio_{family}.png'
        plt.savefig(plot_filename)
        print(f"plot saved: {plot_filename}")
        plt.show()
        plt.close()
