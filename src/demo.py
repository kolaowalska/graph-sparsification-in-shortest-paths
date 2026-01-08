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
    print("==============================================================")
    print("   GRAPH REDUCTION PIPELINE - DESIGN PATTERNS SHOWCASE")
    print("==============================================================")

    # 1. ENTRY POINT: initializing the remote facade
    api = ExperimentFacade()

    # 2. [GATEWAY]: uploading data
    data_path = "src/data/toy.edgelist"
    if not os.path.exists(data_path):
        print(f"error: {data_path} not found")
        return

    print(f"\n[♥] uploading Graph from {data_path}")
    response = api.upload_graph({"path": data_path, "name": "demo_graph", "kind": "file"})
    if response["status"] != "success":
        print("upload failed :( ", response)
        return

    graph_key = response["graph_key"]
    print(f" -> uploaded successfully :) ID: {graph_key}")

    ## [STRATEGY]: random sparsification
    print(f"\n[♥] running sparsification scenario: random sparsifier with (p=0.4)")
    payload_a = {
        "graph_key": graph_key,
        "algorithm": "random",
        "metrics": ["diameter"],
        "params": {"p": 0.4, "seed": 123}
    }
    result_a = api.run_job(payload_a)

    if result_a["status"] == "success":
        data = result_a["data"]
        print(f" -> nodes: {data['nodes_before']} -> {data['nodes_after']}")
        print(f" -> edges: {data['edges_before']} -> {data['edges_after']}")
        print(f" -> metric: {data['metric_results'][0]['summary']}")
    else:
        print("error:", result_a)

    ## [LAYER SUPERTYPE]: graph coarsening
    print(f"\n[♥] running transformation scenario: graph coarsening (merge 50% of nodes)")
    payload_b = {
        "graph_key": graph_key,
        "algorithm": "mock_coarsening",
        "metrics": ["diameter"],
        "params": {"reduction_ratio": 0.5}
    }
    result_b = api.run_job(payload_b)

    if result_b["status"] == "success":
        data = result_b["data"]
        print(f" -> nodes: {data['nodes_before']} -> {data['nodes_after']}")
        print(f" -> edges: {data['edges_before']} -> {data['edges_after']}")
        print(f" -> metric: {data['metric_results'][0]['summary']}")
    else:
        print("error:", result_b)

    # visualization
    if VISUALIZE:
        print("\n[♥] generating visualizations...")
        # cheating here slightly (but for a good cause) for presentation purposes by accessing the internal repo to get objects for plotting
        # TODO: request raw data via API to implement a real facade
        repo = api._service.graph_repo

        g_orig = repo.get(graph_key).to_networkx()

        all_graphs = repo.list_names()

        for name in all_graphs:
            if "random" in name:
                g_sparsified = repo.get(name).to_networkx()
                save_comparison_plot(g_orig, g_sparsified, "sparsification", "demo_sparsify.png")
            elif "coarsened" in name:
                g_coarsened = repo.get(name).to_networkx()
                save_comparison_plot(g_orig, g_coarsened, "coarsening", "demo_coarsen.png")

    print("\n==============================================================")
    print("   DEMO COMPLETED SUCCESSFULLY")
    print("==============================================================")


if __name__ == "__main__":
    main()