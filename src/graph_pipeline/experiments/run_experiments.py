import csv
from pathlib import Path
from tqdm import tqdm
from typing import List, Set

from src.graph_pipeline.utils.parsers import infer_and_parse
from src.graph_pipeline.sparsifiers import sparsifiers_registry
from src.graph_pipeline.utils.flatten_metrics import compute_metrics
from src.graph_pipeline.utils.timer import logger, timer


def main(rho: float = 0.2, data_dir: Path = None, out_file: Path = None, family: str = None):
    out_file.parent.mkdir(parents=True, exist_ok=True)
    samples = list(data_dir.glob("*"))

    if not samples:
        logger.warning(f"no graphs found in directory {data_dir} :(")
        return

    discovered_keys: Set[str] = set()

    logger.info("starting first pass: collecting all possible fieldnames...")
    for file_path in tqdm(samples, desc="collecting fieldnames"):
        try:
            G = infer_and_parse(file_path, family)
            for method_name, sparsifier_func in sparsifiers_registry.items():
                H, _ = timer(sparsifier_func)(G, rho)
                metrics = compute_metrics(G, H, method_name)
                discovered_keys.update(metrics.keys())
        except Exception as e:
            logger.exception(f"error collecting fieldnames from {file_path.name}: {e}")

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

    degree_distribution_keys = sorted([
        key for key in discovered_keys
        if key.startswith('degree_distribution_')
    ])

    fieldnames = base_fieldnames + base_metrics + degree_distribution_keys + ["sparsify_time"]

    expected_fields = set(
        base_fieldnames + base_metrics + degree_distribution_keys + ["sparsify_time"])

    if not discovered_keys.issubset(expected_fields):
        missing_from_order = discovered_keys - expected_fields
        logger.warning(
            f"warning: the following metric keys were discovered "
            f"but not explicitly ordered: {missing_from_order}, "
            f"and they will not appear in the csv.")
        # fieldnames.extend(sorted(list(missing_from_order)))

    logger.info(f"collected {len(fieldnames)} unique fieldnames for csv header")
    # logger.debug(f"final fieldnames: {fieldnames}")

    all_rows_data = []

    logger.info("starting second pass: processing graphs and writing results to csv...")
    for file_path in tqdm(samples, desc="graph processing"):
        try:
            G = infer_and_parse(file_path, family)

            for method_name, sparsifier_fn in sparsifiers_registry.items():
                timed_fn = timer(sparsifier_fn)
                H, elapsed = timed_fn(G, rho)

                metrics = compute_metrics(G, H, method_name)

                row = {
                    "graph": file_path.name,
                    "graph_family": G.graph_family,
                    "method": method_name,
                    "rho": rho,
                    "n": G.n,
                    "m_og": G.m,
                    "m_sparse": H.m,
                    **metrics,
                    "sparsify_time": elapsed
                }
                for field in fieldnames:
                    if field not in row:
                        row[field] = None  # 0.0

                all_rows_data.append(row)

        except Exception as e:
            logger.exception(f"error processing {file_path.name}: {e}")

    with out_file.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_rows_data)

    logger.info(f"results successfully written to {out_file}")


if __name__ == "__main__":
    main()
