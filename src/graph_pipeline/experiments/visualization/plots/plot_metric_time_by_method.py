import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_metric_time_by_method(df: pd.DataFrame, plots_dir: Path):
    if not all(col in df.columns for col in ['metric_time', 'method', 'graph_family']):
        print("skipping 'metric time by method' plot: required columns are missing")
        return

    df = df[df['metric_time'].notna()]

    families = df['graph_family'].unique()
    family_label = ', '.join(sorted(families)) if len(families) <= 3 else 'multiple'

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df,
        x='method',
        y='metric_time',
        hue='method',
        palette='crest',
        errorbar='sd'
    )
    plt.title(f'average metric computation time by method ({family_label} graphs)', fontsize=16)
    plt.ylabel('metric time (s)', fontsize=12)
    plt.xlabel('sparsification method', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    plot_filename = plots_dir / 'metric_time_by_method.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.close()
