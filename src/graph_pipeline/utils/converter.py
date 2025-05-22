import ast
import json
import shutil
from pathlib import Path


def convert_edgelist(input_path: Path, output_path: Path) -> None:
    with input_path.open() as infile, output_path.open("w") as outfile:
        for line in infile:
            parts = line.strip().split(maxsplit=2)

            if len(parts) == 3:
                u, v, raw_weight = parts
                try:
                    weight_data = ast.literal_eval(raw_weight)
                    if isinstance(weight_data, dict) and "weight" in weight_data:
                        weight = weight_data["weight"]
                    else:
                        weight = weight_data
                except (ValueError, SyntaxError):
                    weight = float(raw_weight)
            elif len(parts) == 2:
                u, v = parts
                weight = 1.0
            else:
                continue

            outfile.write(f"{u}\t{v}\t{weight}\n")


def convert_json(input_path: Path, output_path: Path) -> None:
    obj = json.loads(input_path.read_text())
    if isinstance(obj, list):
        obj = obj[0]

    neighbors = obj.get("outList") or obj["inList"]
    weights = obj.get("outWeight") or obj["inWeight"]

    with output_path.open("w") as outfile:
        for u, (nbs, ws) in enumerate(zip(neighbors, weights)):
            for v, w in zip(nbs, ws):
                outfile.write(f"{u}\t{v}\t{w}\n")


def convert_file(input_path: Path, output_path: Path) -> None:
    ext = input_path.suffix.lower()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if ext in {".edgelist", ".txt"}:
        convert_edgelist(input_path, output_path)
    elif ext == ".json":
        convert_json(input_path, output_path)
    elif ext in {".mtx", ".csv"}:
        shutil.copy(input_path, output_path)
    else:
        raise ValueError(f"unsupported graph format for conversion: {ext}")


