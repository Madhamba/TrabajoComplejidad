from abc import ABC


class Action(ABC):
    def __init__(self, caller):
        self.caller = caller
