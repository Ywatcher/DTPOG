from abc import ABC
from typing import Dict, Iterable, Tuple


class Character(ABC):
    def location(self) -> Tuple[str, str]:
        # return cell name
        # and specific location within cell
        pass

    # TODO: ongoing event
