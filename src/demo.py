import sys
import os

sys.path.append(os.getcwd())

from src.interfaces.api import ExperimentFacade

try:
    from src.interfaces.visualizer import save_comparison_plot

    VISUALIZE = True
except ImportError:
    VISUALIZE = False
    print("visualizer not found :( plotting disabled")


def main():

    # ------------------------- CONFIGURATION -------------------------

    METRICS = [
        "diameter",
        "avg_path_length",
        "degree_distribution"
    ]

    SCENARIOS = [
        {
            "label": "Random Sparsifier (p=0.3)",
            "algorithm": "random",
            "params": {"p": 0.3, "seed": 123}
        },
        {
            "label": "K-Neighbor Sparsifier (rho=0.5)",
            "algorithm": "k_neighbor",
            "params": {"rho": 0.5, "seed": 42}
        },
        {
            "label": "Local Degree Sparsifier (rho=0.5)",
            "algorithm": "local_degree",
            "params": {"rho": 0.5}
        },
        {
            "label": "Graph Coarsening (50% node reduction)",
            "algorithm": "mock_coarsening",
            "params": {"reduction_ratio": 0.5}
        }
    ]

    # ---------------------------------------------------------------

    # 1. ENTRY POINT: initializing the remote facade
    api = ExperimentFacade()

    # 2. [GATEWAY]: uploading data
    data_path = "src/data/toy.edgelist"
    if not os.path.exists(data_path):
        print(f"error: {data_path} not found")
        return

    print(f"\n[♥] uploading Graph from {data_path}")
    response = api.upload_graph({
        "path": data_path,
        "name": "demo_graph",
        "kind": "file",
        "directed": True,
        "weighted": True
    })

    if response["status"] != "success":
        print("upload failed :( ", response)
        return

    graph_key = response["graph_key"]
    print(f" → uploaded successfully :) ID: {graph_key}")

    # 3. EXECUTION LOOP
    for i, scenario in enumerate(SCENARIOS, 1):
        label = scenario["label"]
        algo_name = scenario["algorithm"]
        params = scenario["params"]

        print("\n♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥")
        print(f"\n[♥] Scenario {i}/{len(SCENARIOS)}: {label}")

        payload = {
            "graph_key": graph_key,
            "algorithm": algo_name,
            "metrics": METRICS,
            "params": params
        }

        result = api.run_job(payload)

        if result["status"] == "success":
            data = result["data"]
            print(f" • nodes: {data['nodes_before']} → {data['nodes_after']}")
            print(f" • edges: {data['edges_before']} → {data['edges_after']}")
            print(f" • metrics:")

            for m_result in data.get("metric_results", []):
                metric_name = m_result['metric']
                summary = m_result['summary']

                formatted_values = []
                for k, v in summary.items():
                    if isinstance(v, float):
                        formatted_values.append(f"{k} = {v:.4f}")
                    else:
                        formatted_values.append(f"{k} = {v}")

                print(f"    - {metric_name}: {', '.join(formatted_values)}")
        else:
            print(f"error running {algo_name}:", result)


    # 4. VISUALIZATION
    if VISUALIZE:
        print("\n♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥")
        print("\n[♥] generating visualizations\n")
        repo = api._service.graph_repo
        try:
            G = repo.get(graph_key).to_networkx()
            all_graphs = repo.list_names()

            for name in all_graphs:
                if name == graph_key:
                    continue

                label = "modified"
                if "random" in name:
                    label = "random_sparsification"
                elif "neighbor" in name:
                    label = "k_neighbor"
                elif "degree" in name:
                    label = "local_degree"
                elif "coarsen" in name:
                    label = "coarsening"

                g_mod = repo.get(name).to_networkx()
                save_comparison_plot(G, g_mod, label, f"demo_{label}.png")

        except Exception as e:
            print(f"visualization error: {e}")

    print("\n♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ demo completed :) ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥")


if __name__ == "__main__":
    main()