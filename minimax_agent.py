import abc
from agent import Agent
from heuristics import *
import math

MAX_PLAYER = 1
MIN_PLAYER = 2
BOARD_SIZE = 5

SETUP = 0
MOVE = 1
BUILD = 2


class MultiAgentSearchAgent(Agent):
    def __init__(self, evaluation_function, depth=2):
        super().__init__()
        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state, player):
        return


class MinMax(MultiAgentSearchAgent):
    def __init__(self, evaluation_function, depth=2):
        super().__init__(evaluation_function, depth)
        self.max_player = None
        self.min_player = None

    def get_action(self, game_state, player):
        self.max_player = player
        self.min_player = game_state.get_enemy_of(player)
        return self.mini_max(game_state, player)[1]

    def mini_max(self, game_state: Board, player: Player):
        return self.minimax_helper(game_state, player, self.depth * 2)

    def minimax_helper(self, game_state: Board, player: Player, depth):
        if depth == 0 or game_state.is_winner(player):
            enemy_player = game_state.get_enemy_of(player)
            evaluation = self.evaluation_function(game_state, player, enemy_player)
            return evaluation, None

        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0, None

        max_move = None
        if player == self.max_player:
            evaluation = -math.inf
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                score = self.minimax_helper(board_copy, board_copy.get_player_by_number(MIN_PLAYER), depth - 1)[0]
                if score > evaluation:
                    evaluation = score
                    max_move = move
            return evaluation, max_move
        else:
            evaluation = math.inf
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                score = self.minimax_helper(board_copy, board_copy.get_player_by_number(MAX_PLAYER), depth - 1)[0]
                if score < evaluation:
                    evaluation = score
                    max_move = move
            return evaluation, max_move

    def __str__(self):
        return "Minimax Agent"


class AlphaBeta(MultiAgentSearchAgent):
    def __init__(self, evaluation_function, depth=2):
        super().__init__(evaluation_function, depth)
        self.max_player = None
        self.min_player = None

    def get_action(self, game_state: Board, player: Player):
        self.max_player = player
        self.min_player = game_state.get_enemy_of(player)
        return self.alpha_beta(game_state, player)[1]

    def alpha_beta(self, game_state: Board, player: Player):
        return self.alpha_beta_helper(game_state, player, self.depth * 2, -math.inf, math.inf)

    def alpha_beta_helper(self, game_state, player: Player, depth, alpha, beta):
        if depth == 0:
            enemy_player = game_state.get_enemy_of(player)
            evaluation = self.evaluation_function(game_state, player, enemy_player)
            return evaluation, None
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0, None
        if player == self.max_player:
            evaluation = -math.inf
            max_move = None
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                score = self.alpha_beta_helper(board_copy, board_copy.get_player_by_number(MIN_PLAYER), depth - 1,
                                               alpha, beta)[0]
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
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                score = self.alpha_beta_helper(board_copy, board_copy.get_player_by_number(MAX_PLAYER), depth - 1,
                                               alpha, beta)[0]
                if score < evaluation:
                    evaluation = score
                    min_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return evaluation, min_move

    def __str__(self):
        return "Alpha Beta Agent"
