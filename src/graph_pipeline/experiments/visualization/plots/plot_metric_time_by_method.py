import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# average metric computation time by method and graph family
def plot_metric_time_by_method(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['metric_time', 'method', 'graph_family']):
        print("skipping 'metric time by method' plot: required columns are missing")
        return

    df = df[df['metric_time'].notna()]

    grouped = (
        df[df['method'] != 'original']
        .groupby(['graph_family', 'method'], as_index=False)['metric_time']
        .mean()
    )

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=grouped,
        x='method',
        y='metric_time',
        hue='graph_family',
        palette='crest',
        errorbar=None
    )

    # plt.title('average metric computation time by method and graph family', fontsize=16)
    plt.ylabel('metric computation time (s)', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.legend(title='graph family')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    plot_filename = plots_dir / 'metric_time_by_method_and_family.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.close()
