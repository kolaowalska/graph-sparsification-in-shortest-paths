import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# average sparsification time by method and graph family
def plot_sparsification_time(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['sparsify_time', 'method', 'graph_family']):
        print("skipping 'sparsification time' plot: required columns are missing")
        return

    df = df[df['sparsify_time'].notna()]

    grouped = (
        df
        .groupby(['graph_family', 'method'], as_index=False)['sparsify_time']
        .mean()
    )

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=grouped,
        x='method',
        y='sparsify_time',
        hue='graph_family',
        palette="mako",
        errorbar=None
    )

    plt.title('average sparsification time by method', fontsize=16)
    plt.ylabel('sparsification time (s)', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.legend(title='graph family')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    plot_filename = plots_dir / 'sparsify_time_by_method_and_family.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.close()




