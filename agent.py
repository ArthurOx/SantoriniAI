import abc


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state, player):
        return

    def record_iteration(self, state, action, player):
        pass

    def __str__(self):
        pass
