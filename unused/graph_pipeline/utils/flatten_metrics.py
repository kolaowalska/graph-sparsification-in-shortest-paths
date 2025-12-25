from utils.core import GraphWrapper
from metrics.collector import MetricsCollector
from typing import Dict, Union


def compute_metrics(original: GraphWrapper, sparsified: GraphWrapper, method_name: str):
    collector = MetricsCollector(original)
    collector.add(method_name, sparsified)

    results = collector.results[method_name]

    flattened_results = {
        'edges_ratio': results['edges_ratio'],
        'connected_original': results['connected_original'],
        'connected_sparsified': results['connected_sparsified'],
        'diameter_original': results['diameter_original'],
        'diameter_sparsified': results['diameter_sparsified'],
        'unreachable_pairs_ratio': results['unreachable_pairs_ratio'],
        'stretch_avg': results['stretch_avg'],
        'stretch_var': results['stretch_var'],
        'stretch_max': results['stretch_max'],
        'laplacian_qf_original': results['laplacian_qf_original'],
        'laplacian_qf_sparsified': results['laplacian_qf_sparsified'],
    }

    def flatten_degree_distribution(
            prefix: str,
            data: Union[Dict[int, float], Dict[str, Dict[int, float]]],
            target: Dict[str, object]):
        if not data:
            return

        check_format = next(iter(data.values()), None)

        if isinstance(check_format, dict):
            for direction, subdistribution in data.items():
                if subdistribution:
                    for degree, frequency in subdistribution.items():
                        target[f'{prefix}_{direction}_{degree}'] = frequency
        else:
            for degree, frequency in data.items():
                target[f'{prefix}_{degree}'] = frequency

    flatten_degree_distribution('degree_distribution_original', results['degree_distribution_original'], flattened_results)
    flatten_degree_distribution('degree_distribution_sparsified', results['degree_distribution_sparsified'], flattened_results)

    return flattened_results



