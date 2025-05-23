import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Any, Tuple, List

# TODO: debug nonexistent original_row


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


def plot_degree_distributions(df: pd.DataFrame, plots_dir: Path):
    if 'graph' not in df.columns or 'method' not in df.columns or 'graph_family' not in df.columns:
        print("skipping 'degree distribution' plot: required columns are missing.")
        return

    unique_graphs = df['graph'].unique()

    for graph_name in unique_graphs:
        graph_df = df[df['graph'] == graph_name].copy()
        graph_family = graph_df['graph_family'].iloc[0]
        is_directed = (graph_family == 'directed')

        if is_directed:
            fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
            fig.suptitle(f'degree distribution for directed graph: {graph_name}', fontsize=18)

            # Plot original in-degree
            if 'original' in graph_df['method'].values:
                original_row = graph_df[graph_df['method'] == 'original'].iloc[0]

                orig_in_deg_vals, orig_in_freq_vals = _get_degree_data_from_row(
                    original_row, 'degree_distribution_original_in_')
                if orig_in_deg_vals:
                    axes[0].plot(
                        orig_in_deg_vals,
                        orig_in_freq_vals,
                        marker='o',
                        linestyle='-',
                        label='original in-degree',
                        color='black',
                        linewidth=2
                    )

                orig_out_deg_vals, orig_out_freq_vals = _get_degree_data_from_row(
                    original_row, 'degree_distribution_original_out_')
                if orig_out_deg_vals:
                    axes[1].plot(
                        orig_out_deg_vals,
                        orig_out_freq_vals,
                        marker='o',
                        linestyle='-',
                        label='original out-degree',
                        color='black',
                        linewidth=2
                    )

            for method in graph_df['method'].unique():
                if method == 'original':
                    continue
                method_row = graph_df[graph_df['method'] == method].iloc[0]

                spars_in_deg_vals, spars_in_freq_vals = _get_degree_data_from_row(
                    method_row, 'degree_distribution_sparsified_in_')
                if spars_in_deg_vals:
                    axes[0].plot(
                        spars_in_deg_vals,
                        spars_in_freq_vals,
                        marker='x',
                        linestyle='--',
                        label=f'sparsified in-degree ({method})'
                    )

                spars_out_deg_vals, spars_out_freq_vals = _get_degree_data_from_row(
                    method_row, 'degree_distribution_sparsified_out_')
                if spars_out_deg_vals:
                    axes[1].plot(
                        spars_out_deg_vals,
                        spars_out_freq_vals,
                        marker='x',
                        linestyle='--',
                        label=f'sparsified out-degree ({method})'
                    )

            for ax, title in zip(axes, ['in-degree distribution', 'out-degree distribution']):
                ax.set_title(title, fontsize=14)
                ax.set_xlabel('degree', fontsize=12)
                ax.legend(fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.7)

            axes[0].set_ylabel('frequency', fontsize=12)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plot_filename = plots_dir / f'degree_distribution_directed_{graph_name}.png'
            plt.savefig(plot_filename)
            print(f"plot saved: {plot_filename}")
            plt.show()
            plt.close(fig)

        else:  # undirected
            plt.figure(figsize=(12, 7))

            if 'original' in graph_df['method'].values:
                original_row = graph_df[graph_df['method'] == 'original'].iloc[0]
                orig_deg_vals, orig_freq_vals = _get_degree_data_from_row(
                    original_row, 'degree_distribution_original_')
                if orig_deg_vals:
                    plt.plot(
                        orig_deg_vals,
                        orig_freq_vals,
                        marker='o',
                        linestyle='-',
                        label='original',
                        color='black',
                        linewidth=2
                    )

            for method in graph_df['method'].unique():
                if method == 'original':
                    continue
                method_row = graph_df[graph_df['method'] == method].iloc[0]
                spars_deg_vals, spars_freq_vals = _get_degree_data_from_row(
                    method_row, 'degree_distribution_sparsified_')
                if spars_deg_vals:
                    plt.plot(
                        spars_deg_vals,
                        spars_freq_vals,
                        marker='o',
                        linestyle='--',
                        label=f'sparsified ({method})'
                    )

            plt.title(f'degree distribution for undirected graph: {graph_name}', fontsize=16)
            plt.xlabel('degree', fontsize=12)
            plt.ylabel('frequency', fontsize=12)
            plt.legend(fontsize=10)
            plt.grid(True, linestyle='-', alpha=0.7)
            plt.tight_layout()
            plot_filename = plots_dir / f'degree_distribution_undirected_{graph_name}.png'
            plt.savefig(plot_filename)
            print(f"plot saved: {plot_filename}")
            plt.show()
            plt.close()

"""
else:
    plt.figure(figsize=(12, 7))

    if 'original' in graph_df['method'].values:
        original_row = graph_df[graph_df['method'] == 'original'].iloc[0]
        skip_method = 'original'
    else:
        original_row = None
        skip_method = None

    for method in graph_df['method'].unique():
        if method == skip_method:
            continue
        method_row = graph_df[graph_df['method'] == method].iloc[0]

        spars_deg_vals, spars_freq_vals = _get_degree_data_from_row(
            method_row,
            'degree_distribution_sparsified_'
        )

        if spars_deg_vals:
            plt.plot(
                spars_deg_vals,
                spars_freq_vals,
                marker='o',
                linestyle='--',
                label=f'sparsified ({method})'
            )

    # only plot original if found
    if original_row is not None:
        orig_deg_vals, orig_freq_vals = _get_degree_data_from_row(
            original_row,
            'degree_distribution_original_'
        )

        if orig_deg_vals:
            plt.plot(
                orig_deg_vals,
                orig_freq_vals,
                marker='o',
                linestyle='-',
                label='original',
                color='black',
                linewidth=2
            )

    plt.title(f'degree distribution for undirected graph: {graph_name}', fontsize=16)
    plt.xlabel('degree', fontsize=12)
    plt.ylabel('frequency', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='-', alpha=0.7)
    plt.tight_layout()
    plot_filename = plots_dir / f'degree_distribution_undirected_{graph_name}.png'
    plt.savefig(plot_filename)
    print(f"plot saved: {plot_filename}")
    plt.show()
    plt.close()

"""