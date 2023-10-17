from abc import ABC
from enum import Enum
from typing import Dict, Union, List
from demo_games.freddy.actions import *
from user_interfaces.cmd_interface import InputParser, CMDInterface
from demo_games.freddy.events import *


class View(ABC):
    def __eq__(self, __value: object) -> bool:
        raise NotImplemented

    @staticmethod
    def from_obs_list(obs_list: List[Event]) -> "View":
        pass


class RoomView(View):
    def __init__(self, room: str, character_obs: Dict[str, str]) -> None:
        # room: room name
        # character_obs: character and its exact locations in this room
        self.room = room
        self.character_obs = character_obs

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, RoomView):
            return False
        else:
            return self.room == __value.room and \
                     self.character_obs == __value.character_obs

    def __sub__(self, other: "View"):
        # TODO
        return self


class OfficeView(View):
    def __init__(self, office_state: np.ndarray,
                 character_obs: Dict[str, str]) -> None:
        self.character_obs = character_obs
        self.office_state = office_state

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OfficeView):
            return False
        else:
            return np.all(self.office_state == __value.office_state) and \
                        self.character_obs == __value.character_obs


class FreddyCmdParser(InputParser):

    class FreddyCmdActions(Enum):
        checkViewAction = 0

    def __init__(self) -> None:
        super().__init__()
        self._monitor_up = False
        self.CheckViewAction = \
            FreddyCmdParser.FreddyCmdActions.checkViewAction

    def monitor_up(self):
        self._monitor_up = True

    def monitor_down(self):
        self._monitor_up = False

    def parse(self, s: str) -> Union[
            Action,
            None, InputParser._TerminateAction]:
        command_list = s.split(' ')
        command_name = command_list[0]
        args = command_list[1:]
        if command_name in["h" , "help"]:
            return None
        elif command_name in ["q", "quit", "exit"]:
            return self.TerminateAction
        elif command_name in ["v", "view"]:
            # view current obs
            return self.CheckViewAction
        if command_name in ["m"]:
            action = PressButtonAction(EnumButton.monitor)
            return action
        elif command_name in ["mu"]:
            # if monitor down and mu, up and md, or "m"
            action = PressButtonAction(EnumButton.monitor, "up")
            return action
        elif command_name in ["md"]:
            action = PressButtonAction(EnumButton.monitor, "down")
            return action
        elif self._monitor_up:
            return SelectCameraAction(EnumCamera.CAM1A)
        else:
            return PressButtonAction(EnumButton.monitor)


class FreddyCmdInterface(CMDInterface[FreddyCmdParser]):
    input_parser: FreddyCmdParser

    def __init__(self) -> None:
        parser = FreddyCmdParser()
        super().__init__(parser)
        self.current_view = None
        self.prompt = "(five nights at freddy's) "
        self._obs_list = []

    def monitor_up(self):
        self.lock.acquire()
        self.input_parser.monitor_up()
        self.lock.release()

    def monitor_down(self):
        self.lock.acquire()
        self.input_parser.monitor_down()
        self.lock.release()

    def respond(self, parsed_input_obj) -> bool:
        # FIXME : -> respond on cmd action
        if self.input_parser.TerminateAction == parsed_input_obj:
            self.queue.put(FreddyQuitAction())
            print("quit game")
            return True
        elif self.input_parser.CheckViewAction == parsed_input_obj:
            print("check view")
            self.lock.acquire()
            print(self._obs_list)
            self.lock.release()
            # if len(self._obs_list is 0) dont print
            return False
        else:
            self.queue.put(parsed_input_obj)
            return False

    def update_obs(self, obs_list: List[FreddyEvent], _=None):
        # FIXME: use view instead of a List
        self.lock.acquire()
        self._obs_list = obs_list
        # todo: print hint
        self.lock.release()
