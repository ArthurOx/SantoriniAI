from enum import Enum
from move import *
from player import Player
import numpy as np
from copy import copy, deepcopy

BOARD_SIZE = 5
DOME_HEIGHT = 4  # Dome is represented as building of height 4
NUM_PLAYERS = 2


class GamePhase(Enum):
    SETUP = 0
    MOVE = 1
    BUILD = 2


def is_in_board(x: int, y: int):
    if x < 0 or y < 0 or x >= BOARD_SIZE or y >= BOARD_SIZE:
        return False
    return True


class Board:
    def __init__(self, player_1: Player, player_2: Player):
        self._board = np.array([[Tile(j, i) for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)])
        self._phase = GamePhase.SETUP
        self._players_set = 0
        self.player_1 = player_1
        self.player_2 = player_2

    def __hash__(self):
        return hash(self.raw_representation())

    def raw_representation(self):
        result = f'{self._phase.value:2b}'
        for tile in self._board.flatten():
            result += tile.raw_representation()
        return result

    def __eq__(self, other):
        return type(self) == type(other) and (
            np.array_equal(self._board, other._board) and
            self._players_set == other._players_set and
            self.player_1 == other.player_1 and
            self.player_2 == other.player_2
        )

    def clear(self):
        self.player_1.reset()
        self.player_2.reset()
        self.__init__(self.player_1, self.player_2)

    def get_copy(self):
        board_copy = Board(copy(self.player_1), copy(self.player_2))
        board_copy._board = deepcopy(self._board)
        board_copy._phase = self._phase
        board_copy._players_set = self._players_set
        return board_copy

    def get_player_by_number(self, number):
        return self.player_1 if number == 1 else self.player_2

    def get_enemy_of(self, player):
        return self.player_1 if player.number == self.player_2.number else self.player_2

    def get_players(self):
        return self.player_1, self.player_2

    def get_phase(self):
        return self._phase

    def add_move(self, player: Player, move: Move, on_copy=True, save_file=None):
        if on_copy:
            player = self.get_player_by_number(player.number)
            move = copy(move)
        if not self.is_action_valid(player, move):
            raise ValueError(f"Move [{move}] is not allowed")
        if save_file:
            self.record_gameplay(player, move, save_file)

        if self._phase == GamePhase.SETUP:
            self.do_setup(player, move)
            if self._players_set == NUM_PLAYERS:
                self._phase = GamePhase.MOVE

        elif self._phase == GamePhase.MOVE:
            self._phase = GamePhase.BUILD
            self.do_move(player, move)

        elif self._phase == GamePhase.BUILD:
            self._phase = GamePhase.MOVE
            self.do_build(player, move)

    def record_gameplay(self, player, move, save_file):
        if self._phase == GamePhase.SETUP:
            save_file.write(f'Setup: player {player}\n')
            if player.first_piece is None:
                save_file.write(f'p{player}1\t{move.x}\t{move.y}\t{self._board[move.x, move.y].height}\n')
            else:
                save_file.write(f'p{player}2\t{move.x}\t{move.y}\t{self._board[move.x, move.y].height}\n')

        if self._phase == GamePhase.MOVE:
            save_file.write(f'Move: player {player}\n')
            if move.piece == player.first_piece:
                save_file.write(f'p{player}1\t{move.x}\t{move.y}\t{self._board[move.x, move.y].height}\n')
            else:
                save_file.write(f'p{player}2\t{move.x}\t{move.y}\t{self._board[move.x, move.y].height}\n')

        if self._phase == GamePhase.BUILD:
            save_file.write(f'Build: player {player}\n')
            save_file.write(f'build\t{move.x}\t{move.y}\t{self._board[move.x, move.y].height + 1}\n')

    def is_action_valid(self, player: Player, move: Move):
        if self._phase == GamePhase.SETUP:
            return self._is_setup_valid(move)
        if self._phase == GamePhase.MOVE:
            return self._is_move_valid(player, move)
        if self._phase == GamePhase.BUILD:
            return self._is_build_valid(player, move)
        return False

    def _is_setup_valid(self, move: Move):
        if not is_in_board(move.x, move.y) or \
                self.is_occupied(move.x, move.y):
            return False
        return True

    def _is_move_valid(self, player: Player, move: Move):
        if not is_in_board(move.x, move.y) or \
                self.is_occupied(move.x, move.y) or \
                self.is_dome(move.x, move.y) or \
                self._is_illegal_climb(move) or \
                not move.piece or \
                (player.first_piece != move.piece and player.second_piece != move.piece) or \
                move.tile not in self.get_adjacent_tiles(move.piece.tile.x, move.piece.tile.y) or \
                move.piece.player.number != player.number:
            return False
        return True

    def _is_build_valid(self, player: Player, move: Move):
        if not is_in_board(move.x, move.y) or \
                self.is_occupied(move.x, move.y) or \
                self.is_dome(move.x, move.y) or \
                player.moved_piece != move.piece or \
                not move.piece or \
                move.tile not in self.get_adjacent_tiles(move.piece.tile.x, move.piece.tile.y):
            return False
        return True

    def _is_illegal_climb(self, move: Move):
        return self._board[move.x, move.y].height - self._board[move.piece.tile.x, move.piece.tile.y].height > 1

    def is_occupied(self, x: int, y: int):
        return self._board[x, y].piece is not None

    def is_dome(self, x: int, y: int):
        return self._board[x, y].height == DOME_HEIGHT

    """
    Return a list of the tiles around a location
    """
    def get_adjacent_tiles(self, x: int, y: int):
        adjacent = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if is_in_board(x + i, y + j) and not (i == 0 and j == 0):
                    adjacent.append(self._board[x + i, y + j])
        return adjacent

    def get_adjacent_tiles_of_player(self, player: Player):
        return set(self.get_adjacent_tiles(player.first_piece.tile.x, player.first_piece.tile.y) +
                   self.get_adjacent_tiles(player.second_piece.tile.x, player.second_piece.tile.y))

    def do_setup(self, player: Player, move: Move):
        if not player.first_piece:
            player.first_piece = Piece(self._board[move.x, move.y], player)
            self._board[move.x, move.y].piece = player.first_piece
        elif not player.second_piece:
            player.second_piece = Piece(self._board[move.x, move.y], player)
            self._board[move.x, move.y].piece = player.second_piece
            self._players_set += 1
        else:
            raise ValueError("Both pieces already set for player")

    def do_move(self, player: Player, move: Move):
        player.moved_piece = move.piece
        if player.first_piece.tile == move.piece.tile:
            player.first_piece = move.piece
        else:
            player.second_piece = move.piece
        self._board[move.piece.tile.x, move.piece.tile.y].piece = None
        self._board[move.x, move.y].piece = move.piece
        move.piece.tile = move.tile

    def do_build(self, player: Player, move: Move):
        player.moved_piece = None
        self._board[move.x, move.y].add_level()

    def __getitem__(self, coords):
        x, y = coords
        return self._board[x, y]

    def _setup_legal_moves(self, player):
        move_list = []
        if player.first_piece and player.second_piece:
            return move_list
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                move = Move(self._board[x, y])
                if self._is_setup_valid(move):
                    move_list.append(move)
        return move_list

    def _move_legal_moves(self, player):
        move_list = []
        for piece in [player.first_piece, player.second_piece]:
            x, y = piece.tile.x, piece.tile.y
            adjacent = self.get_adjacent_tiles(x, y)
            for tile in adjacent:
                move = Move(tile, piece)
                if self._is_move_valid(player, move):
                    move_list.append(move)
        return move_list

    def _build_legal_moves(self, player):
        move_list = []
        for piece in [player.first_piece, player.second_piece]:
            x, y = piece.tile.x, piece.tile.y
            adjacent = self.get_adjacent_tiles(x, y)
            for tile in adjacent:
                move = Move(tile, piece)
                if self._is_build_valid(player, move):
                    move_list.append(move)
        return move_list

    def get_legal_moves(self, player):
        """
        Returns a list of legal moves for given player for this board state
        """
        move_list = []
        if self._phase == GamePhase.SETUP:
            return self._setup_legal_moves(player)
        elif self._phase == GamePhase.MOVE:
            return self._move_legal_moves(player)
        elif self._phase == GamePhase.BUILD:
            return self._build_legal_moves(player)
        return move_list

    def get_height(self, x: int, y: int):
        return self._board[x, y].height

    def is_on_height_3(self, player):
        if player.first_piece and player.second_piece:
            if player.first_piece.tile.height == 3 or \
                    player.second_piece.tile.height == 3:
                return player
        return None

    def __str__(self):
        board = '╔══╦══╦══╦══╦══╗\n'
        for i in range(BOARD_SIZE):
            board += f'║{self[i, 0]}║{self[i, 1]}║{self[i, 2]}║{self[i, 3]}║{self[i, 4]}║\n'
            if i == BOARD_SIZE - 1:
                break
            board += '╠══╬══╬══╬══╬══╣\n'
        board += '╚══╩══╩══╩══╩══╝\n'
        if self._phase == GamePhase.MOVE:
            board += f'...\n'
        elif self._phase == GamePhase.BUILD:
            board += f'...\n'
        return board
