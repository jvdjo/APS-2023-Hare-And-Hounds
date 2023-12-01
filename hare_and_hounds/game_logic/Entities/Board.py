from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, List, Literal, Dict


class Animal(Enum):
    Hare = 1
    Hound = 2
    

@dataclass
class Board:
    _board: list[list[int]]
    _is_turn: bool
    _total_jogadas: int
    _animal: Animal

    def __init__(self, position: int = 0):
        self._board = [[None for _ in range(3)]
                       for _ in range(5)]
        self._is_turn = position == 0
        self._total_jogadas = 0
        self._animal = Animal.Hare if position == 0 else Animal.Hound
        super().__init__()

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, attributes: Dict):
        board = Board()
        board._board = attributes["_board"]
        board._is_turn = attributes["_is_turn"]
        board._total_jogadas = attributes["_total_jogadas"]
        return board

    def flip(self):
        self._is_turn = not self._is_turn
        return self
