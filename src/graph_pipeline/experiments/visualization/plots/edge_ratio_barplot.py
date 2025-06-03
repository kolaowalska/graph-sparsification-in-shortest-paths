import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# average edge ratio for all families
# DONE

def plot_edge_ratio(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['edges_ratio', 'method', 'graph_family']):
        print("skipping 'edge ratio' plot: required columns are missing")
        return

    df = df[df['edges_ratio'].notna()]

    grouped = (
        df[df['method'] != 'original']
        .groupby(['graph_family', 'method'], as_index=False)['edges_ratio']
        .mean()
    )

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=grouped,
        x='method',
        y='edges_ratio',
        hue='graph_family',
        palette="mako",
        errorbar=None
    )

    # plt.title('average edge ratio', fontsize=16)
    plt.ylabel('edges ratio (m_sparse / m_og)', fontsize=12)
    plt.xlabel('sparsification method (rho = 0.2)', fontsize=12)
    plt.legend(title='graph family')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    plot_filename = plots_dir / 'edges_ratio.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.close()




