import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# average stretch vs. edges ratio
def plot_stretch_vs_edges_ratio(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['stretch_avg', 'edges_ratio', 'method', 'graph_family']):
        print("skipping 'stretch vs edges ratio' plot: required columns are missing")
        return

    # to jest na pale
    families = df['graph_family'].unique()
    family = families[0]

    plt.figure(figsize=(14, 8))
    sns.scatterplot(data=df, x='edges_ratio', y='stretch_avg', hue='method', style='graph_family', s=100, alpha=0.7)
    plt.title(f'average stretch vs. edges ratio for {family} graphs', fontsize=16)
    plt.ylabel('average stretch', fontsize=12)
    plt.xlabel('edges ratio (m_sparse / m_og)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='sparsifier / graph family', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    plot_filename = plots_dir / 'stretch_vs_edges_ratio.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.show()
    plt.close()
