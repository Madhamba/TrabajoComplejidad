from abc import ABC, abstractmethod


class ShortestPathHandle(ABC):
    @abstractmethod
    def get_shortest_path(self, movable):
        pass
