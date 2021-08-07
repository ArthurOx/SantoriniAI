from enum import Enum
from move import *
from player import Player
import numpy as np

BOARD_SIZE = 5
DOME_HEIGHT = 4  # Dome is represented as building of height 4
NUM_PLAYERS = 2


class GamePhase(Enum):
    SETUP = 0
    MOVE = 1
    BUILD = 2


class Board:
    def __init__(self):
        self._board = np.array([[Tile(j, i) for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)])
        self._phase = GamePhase.SETUP
        self._players_set = 0

    def add_move(self, player: Player, move: Move):
        if not self.is_action_valid(player, move):
            raise ValueError("Move is not allowed")

        if self._phase == GamePhase.SETUP:
            piece = self.do_setup(player, move)
            if self._players_set == NUM_PLAYERS:
                self._phase = GamePhase.MOVE
            return piece

        elif self._phase == GamePhase.MOVE:
            self._phase = GamePhase.BUILD
            return self.do_move(player, move)

        elif self._phase == GamePhase.BUILD:
            self._phase = GamePhase.MOVE
            return self.do_build(player, move)

    def is_action_valid(self, player: Player, move: Move):
        if self._phase == GamePhase.SETUP:
            return self._is_setup_valid(move)
        if self._phase == GamePhase.MOVE:
            return self._is_move_valid(player, move)
        if self._phase == GamePhase.BUILD:
            return self._is_build_valid(player, move)
        return False

    def _is_setup_valid(self, move: Move):
        if not self._is_in_grid(move.x, move.y) or \
                self.is_occupied(move.x, move.y):
            return False
        return True

    def _is_move_valid(self, player: Player, move: Move):
        if not self._is_in_grid(move.x, move.y) or \
                self.is_occupied(move.x, move.y) or \
                self.is_dome(move.x, move.y) or \
                self._is_illegal_climb(move) or \
                not move.piece or \
                (player.first_piece != move.piece and player.second_piece != move.piece) or \
                move.tile not in self.get_adjacent_tiles(move.piece.tile.x, move.piece.tile.y) or \
                move.piece.player != player:
            return False
        return True

    def _is_build_valid(self, player: Player, move: Move):
        if not self._is_in_grid(move.x, move.y) or \
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
                if self._is_in_grid(x + i, y + j) and not (i == 0 and j == 0):
                    adjacent.append(self._board[x + i, y + j])
        return adjacent

    def _is_in_grid(self, x: int, y: int):
        if x < 0 or y < 0 or x >= BOARD_SIZE or y >= BOARD_SIZE:
            return False
        return True

    def do_setup(self, player: Player, move: Move):
        if not player.first_piece:
            player.first_piece = Piece(self._board[move.x, move.y], player)
            self._board[move.x, move.y].piece = player.first_piece
            return player.first_piece
        elif not player.second_piece:
            player.second_piece = Piece(self._board[move.x, move.y], player)
            self._board[move.x, move.y].piece = player.second_piece
            self._players_set += 1
            return player.second_piece
        else:
            raise ValueError("Both pieces already set for player")

    def do_move(self, player: Player, move: Move):
        player.moved_piece = move.piece
        self._board[move.piece.tile.x, move.piece.tile.y].piece = None
        self._board[move.x, move.y].piece = move.piece
        move.piece.tile = self._board[move.x, move.y]
        return move.piece

    def do_build(self, player: Player, move: Move):
        player.moved_piece = None
        self._board[move.x, move.y].add_level()
        return move.piece

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




    def __str__(self):
        board = '|@@@|@@@|@@@|@@@|@@@|\n'
        for i in range(BOARD_SIZE):
            board += f'|{self[i, 0]}|{self[i, 1]}|{self[i, 2]}|{self[i, 3]}|{self[i, 4]}|\n'
        board += '|@@@|@@@|@@@|@@@|@@@|\n'
        return board
