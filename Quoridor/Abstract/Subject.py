from abc import ABC, abstractmethod


class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, action):
        for observer in self._observers:
            observer.update(self, action)

