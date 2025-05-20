import csv
from pathlib import Path
from tqdm import tqdm

from src.graph_pipeline.parsers import infer_and_parse
from src.graph_pipeline.sparsifiers import sparsifiers_registry
from src.graph_pipeline.flatten_metrics import compute_metrics
from src.graph_pipeline.utils import logger, timer

DATA_DIR = Path("../data/raw")
OUT_FILE = Path("results/results.csv")


def main(rho=0.2):
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    samples = list(DATA_DIR.glob("*"))

    if not samples:
        logger.warning(f"no graphs found in directory {DATA_DIR} :(")
        return

    all_rows_data = []

    for file_path in tqdm(samples, desc="graph processing"):
        try:
            G = infer_and_parse(file_path)
            for method_name, sparsifier in sparsifiers_registry.items():
                timed_fn = timer(sparsifier)
                H, elapsed = timed_fn(G, rho)
                metrics = compute_metrics(G, H, method_name)

                row = {
                    "graph": file_path.name,
                    "method": method_name,
                    "rho": rho,
                    "n": G.n,
                    "m_og": G.m,
                    "m_sparse": H.m,
                    **metrics,
                    "sparsify_time": elapsed
                }
                all_rows_data.append(row)

        except Exception as e:
            logger.exception(f"error processing {file_path.name}: {e}")

    base_fieldnames = ["graph", "method", "rho", "n", "m_og", "m_sparse"]
    all_keys = set()
    for row_data in all_rows_data:
        all_keys.update(row_data.keys())

    metric_fieldnames = sorted(list(all_keys - set(base_fieldnames) - set(["sparsify_time"])))
    fieldnames = base_fieldnames + metric_fieldnames
    if "sparsify_time" in all_keys:
        fieldnames.append("sparsify_time")
    else:
        if any("sparsify_time" in row for row in all_rows_data):
            fieldnames.append("sparsify_time")

    with OUT_FILE.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                extrasaction='ignore')  # 'extrasaction' = 'ignore' or 'raise'
        writer.writeheader()
        writer.writerows(all_rows_data)

    logger.info(f"results successfully written to {OUT_FILE}")


if __name__ == "__main__":
    main()
