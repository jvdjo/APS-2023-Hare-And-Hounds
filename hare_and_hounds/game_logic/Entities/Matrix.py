import tkinter as tk
from PIL import Image, ImageTk

class Board:
    _board: list[list[int]]
    _is_turn : bool

    def __init__(self, position, board=None):
        self.rows = 3
        self.cols = 5
        self._board = [[None for _ in range(self.rows)] for _ in range(self.cols)]
        self._is_turn = position == 0
        super().__init__()

    def to_dict(self):
        return vars(self)
    
    def from_dict(cls, attributes: dict):
        board = Board()
        board._board = attributes["_board"]
        board._is_turn = attributes["_is_turn"]
        return board