import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


def plot_stretch_vs_edges_ratio(df: pd.DataFrame, plots_dir: Path):
    required = {'stretch_avg', 'edges_ratio', 'method'}
    if not required.issubset(df.columns):
        print("skipping plot: required columns missing:", required - set(df.columns))
        return

    df = df.copy()
    df['edges_ratio'] = pd.to_numeric(df['edges_ratio'], errors='coerce')
    df['stretch_avg'] = pd.to_numeric(df['stretch_avg'], errors='coerce')
    df = df.dropna(subset=['edges_ratio', 'stretch_avg'])
    df = df[np.isfinite(df['edges_ratio']) & np.isfinite(df['stretch_avg'])]

    if df.empty:
        print("no valid data to plot after filtering infinities")
        return

    print(f"Plotting {len(df)} points:")
    print(df[['edges_ratio', 'stretch_avg', 'method']].head())

    plt.figure(figsize=(14, 8))
    sns.scatterplot(
        data=df,
        x='edges_ratio',
        y='stretch_avg',
        hue='method',
        style='method',
        s=100,
        alpha=0.7
    )

    plt.title('average stretch vs. edges ratio for all graphs', fontsize=16)
    plt.xlabel('edges ratio (m_sparse / m_original)', fontsize=12)
    plt.ylabel('average stretch', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='sparsifier', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.88, 1])

    plot_filename = plots_dir / 'stretch_vs_edges_ratio.png'
    plots_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")

    # plt.show()
    plt.close()
