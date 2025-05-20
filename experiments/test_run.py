"""
import csv
from pathlib import Path
from tqdm import tqdm
import logging
from typing import Dict, Any, List, Set

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

    logger.info("starting first pass: collecting possible fieldnames...")
    possible_metrics: Set[str] = set()
    standard_fieldnames: List[str] = ["graph", "graph_family", "method", "rho", "n", "m_og", "m_sparse", "sparsify_time"]
    possible_metrics.update(standard_fieldnames)

    for filepath in tqdm(samples, desc="collecting fieldnames"):
        try:
            G = infer_and_parse(filepath)

            for method_name, sparsifier in sparsifiers_registry.items():
                H, _ = timer(sparsifier)(G, rho)
                metrics = compute_metrics(G, H, method_name)
                possible_metrics.update(metrics.keys())

        except Exception as e:
            logger.exception(f"error collecting fieldnames from {filepath.name}: {e}")

    dynamic_keys = sorted(list(possible_metrics - set(standard_fieldnames)))
    fieldnames = standard_fieldnames + dynamic_keys

    logger.info(f"collected {len(fieldnames)} unique fieldnames for csv header")

    logger.info("starting secong pass: graph processing and writing results to csv...")

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
                        "graph": G.original_filename,
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
                            row[field] = None

                    writer.writerow(row)

            except Exception as e:
                logger.exception(f"error processing {file_path.name}: {e}")

    logger.info(f"results saved to {OUT_FILE}")


if __name__ == "__main__":
    main(rho=0.2)

"""

"""
import csv
from pathlib import Path
from tqdm import tqdm

from src.graph_pipeline.parsers import infer_and_parse
from src.graph_pipeline.sparsifiers import sparsifiers_registry
from src.graph_pipeline.flatten_metrics import compute_metrics
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
                    print("\nprzysiegam zaraz wyrzuce caly ten program wraz z komputerem przez okno")

            except Exception as e:
                logger.exception(f"error processing {file_path.name}: {e}")


if __name__ == "__main__":
    main()


"""