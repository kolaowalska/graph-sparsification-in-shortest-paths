import csv
from pathlib import Path
from tqdm import tqdm

from src.graph_pipeline.parsers import infer_and_parse
from src.graph_pipeline.sparsifiers import sparsifiers_registry
from src.graph_pipeline.metrics import compute_metrics
from src.graph_pipeline.utils import logger, timer

DATA_DIR = Path("../data/raw")
OUT_FILE = Path("results/results.csv")


def main(rho=0.5):
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    samples = list(DATA_DIR.glob("*"))

    if not samples:
        raise ValueError(f"no graphs found in directory {DATA_DIR} :(")

    sample_G = infer_and_parse(samples[0])
    sample_H = sparsifiers_registry[list(sparsifiers_registry.keys())[0]](sample_G, rho)
    sample_metrics = compute_metrics(sample_G, sample_H, list(sparsifiers_registry.keys())[0])

    fieldnames = [
        "graph", "method", "rho", "n", "m_og", "m_sparse",
        *sample_metrics.keys(),
        "sparsify_time"
    ]

    with OUT_FILE.open("w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

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

                    writer.writerow(row)

            except Exception as e:
                logger.exception(f"error processing {file_path.name}: {e}")


if __name__ == "__main__":
    main()
