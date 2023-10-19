from abc import ABC
from enum import Enum
from typing import Dict, Optional, Union, List
from demo_games.freddy.actions import *
from user_interfaces.cmd_interface import InputParser, CMDInterface
from demo_games.freddy.events import *
from user_interfaces.result import *
from demo_games.freddy.game_info.game_map import *


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


_str2cam: Dict[str, EnumCamera] = {
    "1a": EnumCamera.CAM1A,
    "1b": EnumCamera.CAM1B,
    "1c": EnumCamera.CAM1C,
    "2a": EnumCamera.CAMs2A,
    "2b": EnumCamera.CAMs2B,
    "3": EnumCamera.CAM3,
    "4a": EnumCamera.CAMs4A,
    "4b": EnumCamera.CAMs4B,
    "5": EnumCamera.CAM5,
    "6": EnumCamera.CAM6,
    "7": EnumCamera.CAM7
}

# Result of parser:
# menu action
# game action
# interface action
# message


class InterfaceAction(Enum):
    checkViewAction = 0
    checkMapAction = 1


FreddyParseResult = Union[
     Action, MenuAction, Message, InterfaceAction
]


class FreddyCmdParser(InputParser[FreddyParseResult]):

    def __init__(self) -> None:
        super().__init__()
        self._monitor_up = False

    def monitor_up(self):
        self._monitor_up = True

    def monitor_down(self):
        self._monitor_up = False

    def parse(self, s: str) -> Optional[FreddyParseResult]:
        command_list = [w for w in s.split(' ') if len(w) > 0]
        if len(command_list) == 0:
            return None
        command_name = command_list[0]
        args = command_list[1:]
        if command_name in ["h", "help"]:
            return None
        elif command_name in ["q", "quit", "exit"]:
            return MenuAction.quit
        elif command_name in ["v", "view"]:
            # view current obs
            return InterfaceAction.checkViewAction
        elif command_name in ["c"]:
            return InterfaceAction.checkMapAction
        elif command_name in ["m"]:
            action = PressButtonAction(EnumButton.monitor)
            return action
        elif command_name in ["ll"]:
            action = PressButtonAction(EnumButton.leftLight)
        elif command_name in ["rl"]:
            action = PressButtonAction(EnumButton.rightLight)
        elif command_name in ["ld"]:
            action = PressButtonAction(EnumButton.leftDoor)
        elif command_name in ["rd"]:
            action = PressButtonAction(EnumButton.rightDoor)
        elif command_name in ["s"]:
            if len(args) > 0 and args[0].lower() in _str2cam.keys():
                camera_name = _str2cam[args[0].lower()]
                return SelectCameraAction(camera_name)
            else:
                return Message("Invalid args: {}".format(args))
#         elif self._monitor_up:
#             return SelectCameraAction(EnumCamera.CAM1A)
        else:
            return InvalidCommandMessage(s)


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
        if parsed_input_obj == MenuAction.quit:
            self.queue.put(FreddyQuitAction())
            print("quit game")
            return True
        elif parsed_input_obj == InterfaceAction.checkViewAction:
            print("check view")
            self.lock.acquire()
            print(self._obs_list)
            self.lock.release()
            # if len(self._obs_list is 0) dont print
            return False
        elif parsed_input_obj == InterfaceAction.checkMapAction:

            self.lock.acquire()
            print(print_map())
            self.lock.release()
            return False
        elif isinstance(parsed_input_obj, Message):
            print(parsed_input_obj)
        else:
            self.queue.put(parsed_input_obj)
            return False

    def update_obs(self, obs_list: List[FreddyEvent], _=None):
        # FIXME: use view instead of a List
        self.lock.acquire()
        self._obs_list = obs_list
        # todo: print hint
        self.lock.release()
