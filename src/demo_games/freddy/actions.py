from typing import Literal
from demo_games.freddy.enums import EnumAction, EnumCamera, EnumButton

# TODO: distinguish
#   cmd action;
#   game menu action (pause, resume, quit)
#   game action


class Action:
    def __init__(self, action_type: EnumAction) -> None:
        self.action_type = action_type


class PressButtonAction(Action):
    def __init__(
        self,
        button: EnumButton,
        movement: Literal["up", "down", "default"] = "default"
    ):
        super().__init__(EnumAction.PressButton)
        self.button = button
        self.movement = movement


class SelectCameraAction(Action):
    def __init__(self, camera_name: EnumCamera):
        super().__init__(EnumAction.selectCamera)
        self.camera_name = camera_name


class FreddyQuitAction(Action):
    def __init__(self) -> None:
        super().__init__(EnumAction.FreddyQuit)
