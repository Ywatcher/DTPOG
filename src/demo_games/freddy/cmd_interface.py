from typing import Union, List
from demo_games.freddy.actions import *
from user_interfaces.cmd_interface import InputParsesr, CMDInterface
from demo_games.freddy.events import *


class View:
    def __eq__(self, __value: object) -> bool:
        # TODO
        pass


class RoomView(View):
    pass


class OfficeView(View):
    pass


class FreddyCmdParser(InputParsesr):

    def __init__(self) -> None:
        super().__init__()
        self._monitor_up = False

    def monitor_up(self):
        self._monitor_up = True

    def monitor_down(self):
        self._monitor_up = False

    def parse(self, s: str) -> Union[
            Action,
            None, InputParsesr._TerminateAction]:
        if s == "h" or s == "help":
            return None
        elif s in ["q", "quit", "exit"]:
            return self.TerminateAction
        elif s in ["v", "view"]:
            # view current obs
            pass
        elif self._monitor_up:
            return SelectCameraAction(EnumCamera.CAM1A)
        else:
            return PressButtonAction(EnumButton.monitor)


class FreddyCmdInterface(CMDInterface):
    def __init__(self) -> None:
        parser = FreddyCmdParser()
        super().__init__(parser)
        self.current_view = None
        self.prompt = "(five nights at freddy's) "

    def monitor_up(self):
        self.lock.acquire()
        self.input_parser.monitor_up()
        self.lock.release()

    def monitor_down(self):
        self.lock.acquire()
        self.input_parser.monitor_down()
        self.lock.release()

    def update_obs(self, obs_list: List[Event],_=None):
        pass
