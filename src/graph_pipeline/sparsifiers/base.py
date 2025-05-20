from abc import ABC, abstractmethod
from src.graph_pipeline.core import GraphWrapper


class Sparsifier(ABC):
    @abstractmethod
    def name(self) -> str:
        """nazwa"""
        pass

    @abstractmethod
    def sparsify(self, graph: GraphWrapper) -> GraphWrapper:
        """zwraca przerzedzony zesparsyfikowany przesparsyfikowany graf"""
        pass

