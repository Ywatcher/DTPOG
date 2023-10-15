from typing import Dict, Tuple
from framework_.cell import Cell
from framework_.character import Character
from framework_.observation import GamePartialObservation


class Environment:
    def __init__(self) -> None:
        self.all_cells: Dict[str, Cell] = {}
        self.all_characters: Dict[str, Character] = {}

    def add_cell(self, cell: Cell, cell_name: str):
        assert cell_name not in self.all_cells
        self.all_cells.update({cell_name: cell})

    def add_character(self, character: Character, character_name: str):
        assert character_name not in self.all_characters
        self.all_characters.update({character_name: character})

    def update(self):
        pass

    def get_obs(self, character_name: str) -> GamePartialObservation:
        # get full obs if character_name == admin
        pass
