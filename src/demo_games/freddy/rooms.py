import numpy as np
from typing import List, Dict, Optional, Tuple, Iterable, TypedDict
from framework_basic.event import Event
from demo_games.freddy.events import *
from framework_basic.game_object import GameObject


class Room(GameObject[FreddyEvent]):
    def __init__(
            self, name: str,
            locations: Optional[List[str]] = None) -> None:
        super().__init__()
        self.name = name
        if locations is not None:
            self.locations = locations
        else:
            self.locations = ["default"]


class Office(Room):  # player
    def __init__(self) -> None:
        super().__init__(
            name="Office",
            locations=[
                "left door",
                "right door",
                "inside"
            ]
        )

        # ldoor, rdoor, llight, rlight, monitor, power_remaining
        # 0 for door closed/ light off/ monitor off
        self.state = np.array([
            0, 0, 0, 0, 0, 100
        ])

    @property
    def door_closed(self) -> Dict[str, bool]:
        return {"left": self.state[0], "right": self.state[1]}

    @property
    def is_light_on(self) -> Dict[str, bool]:
        return {"left": self.state[2], "right": self.state[3]}

    @property
    def is_monitor_on(self) -> bool:
        return self.state[4]

    @property
    def power_remaining(self) -> int:
        return self.state[5]

        return self.state[4]

    @property
    def device_used(self) -> int:
        return np.sum(self.state[:4])

    def update(self, obs_list: List[FreddyEvent], timer):
        # TODO:
        # if pressed button -> return office state and button flash(1s)
        # end previous obs
        if True:  # if player action in obs_list, door up/close, monitor up/close
            # or light off event
            # or power used up
            # FIXME
            pass
        # if light off or light on:
        # send light off event
        # light off is successor of light on
        # if light on, send observe event to ...
        pass
        # state event should be at last
        e = OfficeInfoEvent(self.state)
        self._event_factory.add_event(e)
        self.send_event(e)


class PirateCove(Room):
    def __init__(self):
        super().__init__(name="PirateCove", locations=["default"])
        self.states = ["hiding", "peering", "to escape"]  # FIXME
        self.state_here = "hiding"



