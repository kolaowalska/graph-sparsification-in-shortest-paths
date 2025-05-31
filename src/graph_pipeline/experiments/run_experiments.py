import csv
from pathlib import Path
from tqdm import tqdm
from typing import List, Set

from utils.parsers import infer_and_parse
from sparsifiers import sparsifiers_registry
from utils.flatten_metrics import compute_metrics
from utils.timer import logger, timer


def main(rho: float = 0.2, data_dir: Path = None, out_file: Path = None, family: str = None):
    out_file.parent.mkdir(parents=True, exist_ok=True)

    samples = list(data_dir.glob("*"))
    if not samples:
        logger.warning(f"no graphs found in directory {data_dir} :(")
        return

    base_fieldnames: List[str] = [
        "graph", "graph_family", "method", "rho", "n", "m_og", "m_sparse"
    ]

    base_metrics: List[str] = [
        'edges_ratio',
        'connected_original',
        'connected_sparsified',
        'diameter_original',
        'diameter_sparsified',
        'unreachable_pairs_ratio',
        'stretch_avg',
        'stretch_var',
        'stretch_max',
        'laplacian_qf_original',
        'laplacian_qf_sparsified',
    ]

    discovered_keys: Set[str] = set()
    rows_data: List[dict] = []

    logger.info("starting metrics computation pass...")
    for file_path in tqdm(
            samples,
            desc="processing graphs",
            ncols=120,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}] {remaining}",
            dynamic_ncols=True
    ):
        try:
            G = infer_and_parse(file_path, family)

            # orig_metrics = compute_metrics(G, G, "original")
            timed_metrics = timer(compute_metrics)
            orig_metrics, metric_time_orig = timed_metrics(G, G, "original")
            discovered_keys.update(orig_metrics.keys())
            row = {
                "graph": file_path.name,
                "graph_family": G.graph_family,
                "method": "original",
                "rho": rho,
                "n": G.n,
                "m_og": G.m,
                "m_sparse": None,
                **orig_metrics,
                "sparsify_time": None,
                "metric_time": metric_time_orig
            }
            rows_data.append(row)

            for method_name, sparsifier_fn in sparsifiers_registry.items():
                timed_fn = timer(sparsifier_fn)
                H, elapsed = timed_fn(G, rho)
                # met = compute_metrics(G, H, method_name)
                timed_metrics = timer(compute_metrics)
                met, metric_time_sparse = timed_metrics(G, H, method_name)
                discovered_keys.update(met.keys())
                row = {
                    "graph": file_path.name,
                    "graph_family": G.graph_family,
                    "method": method_name,
                    "rho": rho,
                    "n": G.n,
                    "m_og": G.m,
                    "m_sparse": H.m,
                    **met,
                    "sparsify_time": elapsed,
                    "metric_time": metric_time_sparse
                }
                rows_data.append(row)

        except Exception as e:
            logger.exception(f"error processing {file_path.name}: {e}")

    degree_distribution_keys = sorted([
        key for key in discovered_keys
        if key.startswith('degree_distribution_')
    ])

    fieldnames = base_fieldnames + base_metrics + degree_distribution_keys + ["sparsify_time", "metric_time"]
    expected_fields = set(fieldnames)

    if not discovered_keys.issubset(expected_fields):
        missing = discovered_keys - expected_fields
        logger.warning(
            f"warning: the following metric keys were discovered but not ordered: {missing}, "
            f"they'll be omitted from the csv file"
        )

    with out_file.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows_data:
            for key in fieldnames:
                row.setdefault(key, None)
            writer.writerow(row)

    logger.info(f"results successfully written to {out_file}")


if __name__ == "__main__":
    main()
