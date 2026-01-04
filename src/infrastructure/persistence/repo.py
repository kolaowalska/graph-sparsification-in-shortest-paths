from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class ExperimentRepository(ABC):
    @abstractmethod
    def save(self, experiment: Experiment):
        pass

    @abstractmethod
    def get(self, run_id: RunID) -> Experiment:
        pass