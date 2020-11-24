import Action.Action


class MoveAction(Action.Action.Action):
    def __init__(self, caller, last_pos, new_pos):
        super().__init__(caller)
        self.last_pos = last_pos
        self.new_pos = new_pos
