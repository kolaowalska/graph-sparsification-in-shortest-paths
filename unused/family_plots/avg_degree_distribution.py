import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Tuple, List


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
    df: pd.DataFrame,
    plots_dir: Path
):
    """
    For each distinct graph_family in `df`, compute the AVERAGE degree‐distribution
    (original vs. each sparsification method) across all graphs in that family,
    and save one figure per family.

    Input `df` must contain:
      - 'graph'            (graph ID, e.g. "foo_01", "foo_02", …)
      - 'graph_family'     (the family string, e.g. "foo")
      - 'method'           (e.g. 'original', 'spannerA', 'spannerB', …)
      - degree‐distribution columns of the form:
          * Undirected:  "degree_distribution_original_<k>" and
                        "degree_distribution_sparsified_<k>"
          * Directed:    "degree_distribution_original_in_<k>",
                        "degree_distribution_original_out_<k>",
                        "degree_distribution_sparsified_in_<k>",
                        "degree_distribution_sparsified_out_<k>"

    For each family:
      1) Collect all rows with method=='original' for graphs in that family.
         Build a dictionary mapping degree→list_of_frequencies, then average.
      2) For each sparsification method M ≠ 'original', do the same (average
         the “sparsified” columns across all graphs in that family).
      3) Plot original vs. each M on a single figure.

    Saves one PNG per family to:
        plots_dir / f"avg_degree_distribution_family_{family}.png"
    """
    required_cols = {'graph', 'graph_family', 'method'}
    if not required_cols.issubset(df.columns):
        print("skipping 'avg degree distributions within family' plot: required columns missing.")
        return

    families = sorted(df['graph_family'].unique())
    if not families:
        print("no families found in DataFrame; nothing to plot.")
        return

    plots_dir.mkdir(parents=True, exist_ok=True)

    for fam in families:
        df_fam = df[df['graph_family'] == fam].copy()
        if df_fam.empty:
            continue

        # Determine whether these are directed‐family or undirected‐family
        # by inspecting if any row has "degree_distribution_original_in_"
        sample = df_fam.iloc[0]
        is_directed = any(col.startswith("degree_distribution_original_in_")
                          for col in sample.index)

        # 1) Compute average ORIGINAL degree distribution across all graphs in this family
        orig_rows = df_fam[df_fam['method'] == 'original']
        if orig_rows.empty:
            print(f"[{fam}] no 'original' rows found; skipping family.")
            continue

        # Build a mapping degree→list_of_freqs, then average
        def _average_dist(rows: pd.DataFrame, prefix: str) -> Tuple[List[int], List[float]]:
            """
            Given a subset of rows (all share same 'method' and same family),
            extract each row’s degree→freq dictionary via _get_degree_data_from_row(row, prefix),
            then build a union of all degrees, and compute the average frequency per degree.
            Returns sorted([degrees], [avg_freqs]).
            """
            # Collect per‐row dicts
            per_row_dicts: List[dict] = []
            for _, r in rows.iterrows():
                degs, freqs = _get_degree_data_from_row(r, prefix)
                per_row_dicts.append(dict(zip(degs, freqs)))

            # Union all degrees
            all_degrees = sorted({d for dmap in per_row_dicts for d in dmap.keys()})
            if not all_degrees:
                return [], []

            # Sum frequencies; if a row is missing a degree, treat freq=0
            sums = {d: 0.0 for d in all_degrees}
            for dmap in per_row_dicts:
                for d in all_degrees:
                    sums[d] += float(dmap.get(d, 0.0))

            n = len(per_row_dicts)
            avg_degs = all_degrees
            avg_freqs = [sums[d] / n for d in all_degrees]
            return avg_degs, avg_freqs

        # Undirected case: prefix_original = "degree_distribution_original_"
        #                 prefix_spars   = "degree_distribution_sparsified_"
        # Directed   case: prefix_original_in  = "degree_distribution_original_in_"
        #                  prefix_original_out = "degree_distribution_original_out_"
        #                  prefix_spars_in     = "degree_distribution_sparsified_in_"
        #                  prefix_spars_out    = "degree_distribution_sparsified_out_"
        fig = None

        if is_directed:
            fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
            fig.suptitle(f"Average degree distribution for directed family: {fam}", fontsize=18)

            # A) Original In‐degree
            orig_degs_in, orig_freqs_in = _average_dist(orig_rows, "degree_distribution_original_in_")
            if orig_degs_in:
                axes[0].plot(
                    orig_degs_in,
                    orig_freqs_in,
                    marker='o',
                    linestyle='-',
                    color='black',
                    linewidth=2,
                    label='original-in'
                )
            # B) Original Out‐degree
            orig_degs_out, orig_freqs_out = _average_dist(orig_rows, "degree_distribution_original_out_")
            if orig_degs_out:
                axes[1].plot(
                    orig_degs_out,
                    orig_freqs_out,
                    marker='o',
                    linestyle='-',
                    color='black',
                    linewidth=2,
                    label='original-out'
                )

            # 2) For each sparsification method, average its in/out distributions
            methods = sorted(set(df_fam['method'].unique()) - {'original'})
            for method in methods:
                spars_rows = df_fam[df_fam['method'] == method]
                if spars_rows.empty:
                    continue

                # Sparsified In‐degree
                spars_degs_in, spars_freqs_in = _average_dist(spars_rows, "degree_distribution_sparsified_in_")
                if spars_degs_in:
                    axes[0].plot(
                        spars_degs_in,
                        spars_freqs_in,
                        marker='x',
                        linestyle='--',
                        label=f"sparsified-in ({method})"
                    )

                # Sparsified Out‐degree
                spars_degs_out, spars_freqs_out = _average_dist(spars_rows, "degree_distribution_sparsified_out_")
                if spars_degs_out:
                    axes[1].plot(
                        spars_degs_out,
                        spars_freqs_out,
                        marker='x',
                        linestyle='--',
                        label=f"sparsified-out ({method})"
                    )

            # Finalize axes
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
            # Undirected family: single subplot
            fig = plt.figure(figsize=(12, 7))

            # A) Original
            orig_degs, orig_freqs = _average_dist(orig_rows, "degree_distribution_original_")
            if orig_degs:
                plt.plot(
                    orig_degs,
                    orig_freqs,
                    marker='o',
                    linestyle='-',
                    color='black',
                    linewidth=2,
                    label='original'
                )

            # B) Each sparsification method
            methods = sorted(set(df_fam['method'].unique()) - {'original'})
            for method in methods:
                spars_rows = df_fam[df_fam['method'] == method]
                if spars_rows.empty:
                    continue

                spars_degs, spars_freqs = _average_dist(spars_rows, "degree_distribution_sparsified_")
                if spars_degs:
                    plt.plot(
                        spars_degs,
                        spars_freqs,
                        marker='o',
                        linestyle='--',
                        label=f"sparsified ({method})"
                    )

            plt.title(f"Average degree distribution for family: {fam}", fontsize=16)
            plt.xlabel("degree", fontsize=12)
            plt.ylabel("avg frequency", fontsize=12)
            plt.legend(fontsize=10)
            plt.grid(True, linestyle='-', alpha=0.7)
            plt.tight_layout()

        # 3) Save figure
        fname = plots_dir / f"avg_degree_distribution_family_{fam}.png"
        fig.savefig(fname)
        print(f"plot saved: {fname}")
        plt.close(fig)
