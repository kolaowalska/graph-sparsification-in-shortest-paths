from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from domain.metrics.base import MetricResult


# DATA TRANSFER OBJECT

@dataclass(frozen=True)
class ExperimentDTO:
    """
    a container to move experiment data from the service layer to cli/ui without exposing domain entities
    """
    graph_name: str
    nodes_before: int
    edges_before: int
    nodes_after: int
    edges_after: int
    sparsifier_name: str
    metric_results: List[MetricResult]

    metadata: Dict[str, Any] # miejsce na wszystkie moje szalone pomysly :)

