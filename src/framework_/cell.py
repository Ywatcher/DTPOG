from abc import ABC
from typing import Dict, Iterable, Tuple


class Cell(ABC):
    @property
    def locations_within(self) -> Iterable[str]:
        pass
    pass


