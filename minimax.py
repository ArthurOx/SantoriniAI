import abc
from board import *
from player import Player
import util
import math

MAX_PLAYER = 0
MIN_PLAYER = 1
BOARD_SIZE = 5


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state, player):
        return

    def stop_running(self):
        pass


class MultiAgentSearchAgent(Agent):
    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state, player):
        return


def tile_value(game_state, x: int, y: int):
    if not Board._is_in_grid(game_state, x, y):
        return
    if x == 0 or x == 4:
        return 1
    if x == 1 or x == 3:
        if y == 0 or y == 4:
            return 1
        else:
            return 2
    else:
        if y == 0 or y == 4:
            return 1
        if y == 1 or y == 3:
            return 2
        else:
            return 4


def evaluation_function(game_state):
    score = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            score += Board.get_height(game_state, i, j) * tile_value(game_state, i, j)
    return score


class MinMax(MultiAgentSearchAgent):
    def get_action(self, game_state, player: Player):
        return self.minimax_helper(game_state, player, self.depth * 2)

    def minimax_helper(self, game_state, player, depth):
        successors = []
        if depth == 0:
            evaluation = self.evaluation_function(game_state)
            return evaluation
        # evaluation = -math.inf if player == MAX_PLAYER else math.inf
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0
        if player == MAX_PLAYER:
            evaluation = -math.inf
            for move in legal_moves:
                score = self.minimax_helper(game_state.do_move(player, move), MIN_PLAYER, depth - 1)
                evaluation = max(evaluation, score)
            return evaluation
        else:
            evaluation = math.inf
            for move in legal_moves:
                score = self.minimax_helper(game_state.do_move(player, move), MAX_PLAYER, depth - 1)
                evaluation = min(evaluation, score)
            return evaluation


class AlphaBeta(MultiAgentSearchAgent):
    def get_action(self, game_state, player: Player):
        return self.alpha_beta_helper(game_state, player, self.depth * 2, -math.inf, math.inf)

    def alpha_beta_helper(self, game_state, player, depth, alpha, beta):
        if depth == 0:
            evaluation = self.evaluation_function(game_state)
            return evaluation
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0
        if player == MAX_PLAYER:
            evaluation = -math.inf
            for move in legal_moves:
                score = self.alpha_beta_helper(game_state.do_move(player, move), MIN_PLAYER, depth - 1, alpha, beta)
                evaluation = max(evaluation, score)
                alpha = max(alpha, evaluation)
                if alpha >= beta:
                    break
            return evaluation
        else:
            evaluation = math.inf
            for move in legal_moves:
                score = self.alpha_beta_helper(game_state.do_move(player, move), MAX_PLAYER, depth - 1, alpha, beta)
                evaluation = min(evaluation, score)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return evaluation
