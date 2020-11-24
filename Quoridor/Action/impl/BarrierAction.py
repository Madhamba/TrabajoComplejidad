import Action.Action


class BarrierAction(Action.Action.Action):
    def __init__(self, caller, edge1, edge2):
        super().__init__(caller)
        self.edge1 = edge1
        self.edge2 = edge2
