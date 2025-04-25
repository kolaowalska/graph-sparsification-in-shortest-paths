from abc import ABC, abstractmethod
from graphs.graph import Graph


class Sparsifier(ABC):
    @abstractmethod
    def name(self) -> str:
        """nazwa"""
        pass

    @abstractmethod
    def sparsify(self, graph: Graph) -> Graph:
        """zwraca przerzedzony zesparsyfikowany przesparsyfikowany graf"""
        pass

