from enum import Enum
import numpy as np
from demo_games.freddy.enums import EnumAction, EnumCamera, EnumButton

class Action:
    def __init__(self, action_type: EnumAction) -> None:
        self.action_type = action_type


class PressButtonAction(Action):
    def __init__(self, button: EnumButton):
        super().__init__(EnumAction.PressButton)
        self.button = button


class SelectCameraAction(Action):
    def __init__(self, camera_name: EnumCamera):
        super().__init__(EnumAction.selectCamera)
        self.camera_name = camera_name


