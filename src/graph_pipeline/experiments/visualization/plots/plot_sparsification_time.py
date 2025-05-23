import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# average sparsification time by method and graph family
def plot_sparsification_time(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['sparsify_time', 'method', 'graph_family']):
        print("skipping 'sparsification time' plot: required columns are missing")
        return

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df,
        x='method',
        y='sparsify_time',
        hue='method',
        palette="mako",
        errorbar=None
    )
    plt.title('average sparsification time by method', fontsize=16)
    plt.ylabel('time (s)', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.legend(title='graph family', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    plot_filename = plots_dir / 'sparsify_time_by_method_family.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.show()
    plt.close()
