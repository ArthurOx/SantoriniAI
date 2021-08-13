import numpy as np
import abc
from board import *
from player import Player
from agent import Agent
from heuristics import *
import util
import math

MAX_PLAYER = 0
MIN_PLAYER = 1
BOARD_SIZE = 5

SETUP = 0
MOVE = 1
BUILD = 2


class MultiAgentSearchAgent(Agent):
    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        super().__init__()
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state, player):
        return


class MinMax(MultiAgentSearchAgent):
    def __init__(self, player_1: Player, player_2: Player):
        super().__init__()
        self.player_1 = player_1
        self.player_2 = player_2

    def get_action(self, game_state, player):
        return self.mini_max(game_state, player)[1]

    def mini_max(self, game_state, player: Player):
        return self.minimax_helper(game_state, player, self.depth * 2)

    def minimax_helper(self, game_state, player, depth):
        if depth == 0:
            enemy_player = self.player_1 if player == self.player_2 else self.player_2
            evaluation = self.evaluation_function(game_state, player, enemy_player)
            return evaluation, None
        max_move = None
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0, None
        if player == MAX_PLAYER:
            evaluation = -math.inf
            for move in legal_moves:
                score = self.minimax_helper(game_state.do_move(player, move), MIN_PLAYER, depth - 1)
                # evaluation = max(evaluation, score)
                if score > evaluation:
                    evaluation = score
                    max_move = move
            return evaluation, max_move
        else:
            evaluation = math.inf
            for move in legal_moves:
                score = self.minimax_helper(game_state.do_move(player, move), MAX_PLAYER, depth - 1)
                # evaluation = min(evaluation, score)
                if score < evaluation:
                    evaluation = score
                    max_move = move
            return evaluation, max_move

    def __str__(self):
        return "Minimax Agent"


class AlphaBeta(MultiAgentSearchAgent):
    def __init__(self, player_1: Player, player_2: Player):
        super().__init__()
        self.player_1 = player_1
        self.player_2 = player_2

    def get_action(self, game_state, player):
        return self.alpha_beta(game_state, player)[1]

    def alpha_beta(self, game_state, player: Player):
        return self.alpha_beta_helper(game_state, player, self.depth * 2, -math.inf, math.inf)

    def alpha_beta_helper(self, game_state, player, depth, alpha, beta):
        if depth == 0:
            enemy_player = self.player_1 if player == self.player_2 else self.player_2
            evaluation = self.evaluation_function(game_state, player, enemy_player)
            return evaluation, None
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0, None
        if player == MAX_PLAYER:
            evaluation = -math.inf
            max_move = None
            for move in legal_moves:
                score = self.alpha_beta_helper(game_state.do_move(player, move), MIN_PLAYER, depth - 1, alpha, beta)
                # evaluation = max(evaluation, score)
                if score > evaluation:
                    evaluation = score
                    max_move = move
                alpha = max(alpha, evaluation)
                if alpha >= beta:
                    break
            return evaluation, max_move
        else:
            evaluation = math.inf
            min_move = None
            for move in legal_moves:
                score = self.alpha_beta_helper(game_state.do_move(player, move), MAX_PLAYER, depth - 1, alpha, beta)
                # evaluation = min(evaluation, score)
                if score < evaluation:
                    evaluation = score
                    min_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return evaluation, min_move

    def __str__(self):
        return "Alpha Beta Agent"
