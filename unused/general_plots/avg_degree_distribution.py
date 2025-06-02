import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Tuple, List
# from ../visualization.utils.get_degree_data import _get_degree_data_from_row


def _get_degree_data_from_row(row: pd.Series, cols_prefix: str) -> Tuple[List[int], List[float]]:
    if cols_prefix.endswith('_'):
        relevant_cols = [col for col in row.index if col.startswith(cols_prefix) and pd.notna(row[col])]
    else:
        relevant_cols = [col for col in row.index if col.startswith(cols_prefix)
                         and not col.startswith(f'{cols_prefix}in_')
                         and not col.startswith(f'{cols_prefix}out_')
                         and pd.notna(row[col])]

    degrees_dict = {}
    for col in relevant_cols:
        try:
            degree = int(col.split('_')[-1])
            degrees_dict[degree] = row[col]
        except ValueError:
            pass

    sorted_degrees = sorted(degrees_dict.items())
    return [d[0] for d in sorted_degrees], [d[1] for d in sorted_degrees]


def plot_avg_degree_distributions(
    df_agg: pd.DataFrame,
    plots_dir: Path
):
    required_cols = {'graph_family', 'method'}
    if not required_cols.issubset(df_agg.columns):
        print("skipping 'avg degree distribution across families' plot: required columns missing.")
        return

    # Keep only the 'original' rows
    df_orig_fam = df_agg[df_agg['method'] == 'original'].copy()
    if df_orig_fam.empty:
        print("skipping: no 'original' rows in aggregated DataFrame.")
        return

    # Detect directed vs. undirected by checking column prefixes in df_agg
    sample = df_agg.iloc[0]
    is_directed = any(col.startswith("degree_distribution_original_in_") for col in sample.index)

    plots_dir.mkdir(parents=True, exist_ok=True)

    if is_directed:
        fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
        fig.suptitle("Average original degree distributions: all families (directed)", fontsize=18)

        # Plot each family’s already‐averaged distribution
        for _, row in df_orig_fam.iterrows():
            fam = row['graph_family']
            degs_in, freqs_in = _get_degree_data_from_row(row, "degree_distribution_original_in_")
            degs_out, freqs_out = _get_degree_data_from_row(row, "degree_distribution_original_out_")

            if degs_in:
                axes[0].plot(
                    degs_in,
                    freqs_in,
                    marker='o',
                    linestyle='-',
                    label=fam
                )
            if degs_out:
                axes[1].plot(
                    degs_out,
                    freqs_out,
                    marker='o',
                    linestyle='-',
                    label=fam
                )

        axes[0].set_title("In‐degree distribution", fontsize=14)
        axes[0].set_xlabel("degree", fontsize=12)
        axes[0].set_ylabel("avg frequency", fontsize=12)
        axes[0].legend(fontsize=10)
        axes[0].grid(True, linestyle='--', alpha=0.7)

        axes[1].set_title("Out‐degree distribution", fontsize=14)
        axes[1].set_xlabel("degree", fontsize=12)
        axes[1].legend(fontsize=10)
        axes[1].grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    else:
        plt.figure(figsize=(12, 7))
        plt.title("Average original degree distributions: all families (undirected)", fontsize=16)

        for _, row in df_orig_fam.iterrows():
            fam = row['graph_family']
            degs, freqs = _get_degree_data_from_row(row, "degree_distribution_original_")
            if degs:
                plt.plot(
                    degs,
                    freqs,
                    marker='o',
                    linestyle='-',
                    label=fam
                )

        plt.xlabel("degree", fontsize=12)
        plt.ylabel("avg frequency", fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='-', alpha=0.7)
        plt.tight_layout()

    filename = plots_dir / "avg_degree_distribution_all_families.png"
    plt.savefig(filename)
    print(f"plot saved: {filename}")
    plt.close()