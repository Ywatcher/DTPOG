from enum import Enum
import numpy as np


class EnumCamera(Enum):
    CAM1A = 1  # -> ShowStage  #0 for b, c, fr
    CAM1B = 2  # -> DiningArea  #1 for bonnie, chicka, freddy; 2 for b, c close
    CAM1C = 3  # -> PirateCove  #0 for fo-0, 1 for fo-1, 2 .. 3 .. =foxy not here at stage 3
    CAMs2A = 4  # -> WestHallA  #5 for b
    CAMs2B = 5  # -> WestHallB  #7 for b, 3 for foxy = foxy run
    CAM3 = 6  # -> SupplyCloset  #6 for b
    CAMs4A = 7  # -> EastHallA  #5 for c, 3 for fr, 6 for c close
    CAMs4B = 8  # -> EastHallB  #7 for c, 4 for fr
    CAM5 = 9  # -> Backstage  #3 for b, 4 for b close,
    CAM6 = 10  # -> Kitchen
    CAM7 = 11  # -> Restrooms  #3 for c, 4 for c close, 2 for fr
    OfficeView = 12  # Office
    # office is not camera; yet we include it to out enumeration without a
    # loss of generality
    NONE = 0

    def room(self) -> str:
        return ["NONE",
                "ShowStage", "DiningArea", "PirateCove",
                "WestHallA", "WestHallB", "SupplyCloset",
                "EastHallA", "EastHallB", "Backstage",
                "Kitchen", "Restrooms", "Office"
                ][self.value]

# public enum EnumObservation {
    # ShowStage, //0 for b, c, fr
    # DiningArea, //1 for bonnie, chica, freddy; 2 for b, c close
    # DiningAreaFar,
    # DiningAreaClose,
    # PirateCoveHiding,
    # PirateCovePeering, //0 for fo-0, 1 for fo-1, 2 .. 3 .. (foxy not here at stage 3)
    # PirateCoveToEscape,
    # WestHallA, //5 for b
    # WestHallB, //7 for b, 3 for foxy ( foxy run)
    # SupplyCloset, //6 for b
    # EastHallA, //5 for c, 3 for fr, 6 for c close
    # EastHallAFar,
    # EastHallAClose,
    # EastHallB, //7 for c, 4 for fr
    # BackstageFar, //3 for b, 4 for b close,
    # BackstageClose,
    # Kitchen,
    # Restrooms, //3 for c, 4 for c close, 2 for fr
    # RestroomsFar,
    # RestroomsClose,
    # OfficeLeft, // bonnie
    # OfficeRight, // chica
    # None
# }


class EnumAction(Enum):
    selectCamera = 0
    PressButton = 1
    FreddyQuit = 3
    # stop


class EnumButton(Enum):
    leftDoor = 1 #np.array([1, 0, 0, 0, 0, 0])
    rightDoor = 2 # np.array([0, 1, 0, 0, 0, 0])
    leftLight = 3 #np.array([0, 0, 1, 0, 0, 0])
    rightLight = 3 #np.array([0, 0, 0, 1, 0, 0])
    monitor = 5 #np.array([0, 0, 0, 0, 1, 0])


if __name__ == "__main__":
    # print(type(a))
    # print(isinstance(a, EnumAction))
    # resume

    pass
