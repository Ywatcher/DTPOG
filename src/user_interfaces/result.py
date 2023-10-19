from abc import ABC
from enum import Enum
from typing import Type, TypeVar


class GameAction(ABC):
    pass


class MenuAction(Enum):
    #     pause = 0
    #     resume = 1
    quit = 2


class Message:
    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return self.message


class InvalidCommandMessage(Message):
    def __init__(self, command: str) -> None:
        super().__init__("Invalid command: {}".format(command))


ParseResult = TypeVar(
    "ParseResult",
    Type[GameAction], MenuAction, Type[Message], object
)
