import abc
from agent import Agent
from heuristics import *
import math

SETUP = 0
MOVE = 1
BUILD = 2

class HeuristicSearchAgent(Agent):
    def __init__(self, evaluation_function, depth=2):
        super().__init__()
        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state, player):
        return


class MinMax(HeuristicSearchAgent):
    def __init__(self, evaluation_function, depth=2):
        super().__init__(evaluation_function, depth)
        self.max_player = 1
        self.min_player = 2
        self.move_action = None
        self.build_action = None

    def get_action(self, game_state, player):
        self.max_player = player.number
        self.min_player = 2 if player.number == 1 else 1
        if not self.move_action:
            self.mini_max(game_state, player)
            return self.move_action
        second_action = self.build_action
        self.move_action, self.build_action = None, None
        return second_action

    def mini_max(self, game_state, player: Player):
        # During setup limit the search depth to 2
        if game_state.get_phase() == GamePhase.SETUP:
            _, self.move_action, self.build_action = self.minimax_helper(game_state, player, 2)
        else:
            _, self.move_action, self.build_action = self.minimax_helper(game_state, player, self.depth)

    def minimax_helper(self, game_state: Board, player: Player, depth):
        max_player = game_state.get_player_by_number(self.max_player)
        min_player = game_state.get_player_by_number(self.min_player)

        if game_state.get_phase() is not GamePhase.SETUP and not game_state.get_legal_moves(min_player):
            evaluation = self.evaluation_function(game_state, max_player, min_player)
            return evaluation, None
        elif depth == 0 or game_state.is_on_height_3(max_player):
            evaluation = self.evaluation_function(game_state, max_player, min_player)
            return evaluation, None

        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0, None

        if player.number == self.max_player:
            evaluation = -math.inf
            max_move, max_build = None, None
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                # If we moved we can always build on the square we moved from, so there are always legal moves
                legal_builds = board_copy.get_legal_moves(board_copy.get_player_by_number(self.max_player))
                for build in legal_builds:
                    board_copy_2 = board_copy.get_copy()
                    board_copy_2.add_move(player, build)
                    score = self.minimax_helper(board_copy_2, board_copy_2.get_player_by_number(self.min_player),
                                                depth - 1)[0]
                    if score > evaluation:
                        evaluation = score
                        max_move, max_build = move, build
            return evaluation, max_move, max_build
        else:
            evaluation = math.inf
            max_move, max_build = None, None
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                legal_builds = board_copy.get_legal_moves(board_copy.get_player_by_number(self.min_player))
                for build in legal_builds:
                    board_copy_2 = board_copy.get_copy()
                    board_copy_2.add_move(player, build)
                    score = self.minimax_helper(board_copy_2, board_copy_2.get_player_by_number(self.max_player),
                                                depth - 1)[0]
                    if score < evaluation:
                        evaluation = score
                        max_move, max_build = move, build
            return evaluation, max_move, max_build

    def reset_minimax(self):
        self.build_action = None
        self.move_action = None

    def __str__(self):
        return "Minimax Agent"


class AlphaBeta(HeuristicSearchAgent):
    def __init__(self, evaluation_function, depth=4):
        super().__init__(evaluation_function, depth)
        self.max_player = 1
        self.min_player = 2
        self.move_action = None
        self.build_action = None

    def get_action(self, game_state: Board, player: Player):
        self.max_player = player.number
        self.min_player = 2 if player.number == 1 else 1
        if not self.move_action:
            self.alpha_beta(game_state, player)
            return self.move_action
        second_action = self.build_action
        self.move_action, self.build_action = None, None
        return second_action

    def alpha_beta(self, game_state: Board, player: Player):
        # During setup limit the search depth to 2
        if game_state.get_phase() == GamePhase.SETUP:
            _, self.move_action, self.build_action = self.alpha_beta_helper(game_state, player, 2, -math.inf,
                                                                            math.inf)
        else:
            _, self.move_action, self.build_action = self.alpha_beta_helper(game_state, player, self.depth,
                                                                            -math.inf, math.inf)

    def alpha_beta_helper(self, game_state, player: Player, depth, alpha, beta):
        max_player = game_state.get_player_by_number(self.max_player)
        min_player = game_state.get_player_by_number(self.min_player)
        if depth == 0 or game_state.is_on_height_3(max_player):
            evaluation = self.evaluation_function(game_state, max_player, min_player)
            return evaluation, None
        elif game_state.get_phase() is not GamePhase.SETUP and not game_state.get_legal_moves(min_player):
            evaluation = self.evaluation_function(game_state, max_player, min_player)
            return evaluation, None
        legal_moves = game_state.get_legal_moves(player)
        if not legal_moves:
            return 0, None

        if player.number == self.max_player:
            evaluation = -math.inf
            max_move, max_build = None, None
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                # If we moved we can always build on the square we moved from, so there are always legal moves
                legal_builds = board_copy.get_legal_moves(board_copy.get_player_by_number(self.max_player))
                for build in legal_builds:
                    board_copy_2 = board_copy.get_copy()
                    board_copy_2.add_move(player, build)
                    score = self.alpha_beta_helper(board_copy_2, board_copy_2.get_player_by_number(self.min_player),
                                                   depth - 1, alpha, beta)[0]
                    if score > evaluation:
                        evaluation = score
                        max_move, max_build = move, build
                    if score >= beta:
                        break
                    alpha = max(alpha, score)
                else:
                    continue
                break
            return evaluation, max_move, max_build
        else:
            evaluation = math.inf
            min_move, min_build = None, None
            for move in legal_moves:
                board_copy = game_state.get_copy()
                board_copy.add_move(player, move)
                legal_builds = board_copy.get_legal_moves(board_copy.get_player_by_number(self.min_player))
                for build in legal_builds:
                    board_copy_2 = board_copy.get_copy()
                    board_copy_2.add_move(player, build)
                    score = self.alpha_beta_helper(board_copy_2, board_copy_2.get_player_by_number(self.max_player),
                                                   depth - 1, alpha, beta)[0]
                    if score < evaluation:
                        evaluation = score
                        min_move, min_build = move, build
                    if score <= alpha:
                        break
                    beta = min(beta, evaluation)
                else:
                    continue
                break
            return evaluation, min_move, min_build

    def __str__(self):
        return "Alpha Beta Agent"

    def reset_minimax(self):
        self.build_action = None
        self.move_action = None
