import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# average stretch per sparsification method
def plot_avg_stretch_vs_sparsifier(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['stretch_avg', 'method', 'graph_family']):
        print("skipping 'stretch vs edges ratio' plot: required columns are missing")
        return

    # to jest na pale
    families = df['graph_family'].unique()
    family = families[0]

    plt.figure(figsize=(10, 8))
    sns.boxplot(data=df, x='method', y='stretch_avg', palette='viridis')
    plt.title(f'average stretch by sparsification method for {family} graphs', fontsize=16)
    plt.ylabel('average stretch', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    # plt.legend(title='graph family', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    plot_filename = plots_dir / 'stretch_per_sparsifier.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.show()
    plt.close()
