from typing import List, Optional, Dict

from src.infrastructure.persistence.repo import GraphRepository, ExperimentRepository
from src.domain.graph_model import Graph
from src.domain.experiment import Experiment, RunID

class InMemoryGraphRepository(GraphRepository):
    def __init__(self):
        self._storage: Dict[str, Graph] = {}

    def save(self, graph: Graph) -> None:
        self._storage[graph.id] = graph

    def get(self, name: str) -> Optional[Graph]:
        return self._storage.get(name)

    def list_names(self) -> List[str]:
        return sorted(list(self._storage.keys()))


class InMemoryExperimentRepository(ExperimentRepository):
    def __init__(self):
        self._storage: Dict[RunID, Experiment] = {}

    def save(self, experiment: Experiment) -> None:
        self._storage[experiment.run_id] = experiment

    def get(self, run_id: RunID) -> Optional[Experiment]:
        return self._storage.get(run_id)