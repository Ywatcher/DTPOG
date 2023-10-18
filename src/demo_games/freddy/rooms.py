import numpy as np
from typing import List, Dict, Optional, Tuple, Iterable, TypedDict
from demo_games.freddy.actions import PressButtonAction
from framework_basic.event import Event
from demo_games.freddy.events import *
from framework_basic.game_object import GameObject

door_movement_time = 5


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
        # ldoor moving, rdoor moving, monitor moving
        # 0 for door open/ light off/ monitor off / not moving
        self.state = np.array([
            0, 0, 0, 0, 0, 100, 0, 0, 0
        ])
        self.current_camera_name: EnumCamera = EnumCamera.CAM1A  # showstage
        self.current_obs_event: ObserveEvent = None
        self.to_send_obs = True
        # below events are set to no one.
        self.door_event: Dict[str, Optional[DeviceMovementEvent]] \
            = {"left": None, "right": None}
        self.monitor_event: Optional[DeviceMovementEvent] = None
        self.light_event: Dict[str, Optional[LightDurationEvent]] \
            = {"left": None, "right": None}
        self.no_power_is_set = False  # TODO: rename

    @property
    def current_view(self) -> EnumCamera:
        if self.is_monitor_on:
            return self.current_camera_name
        else:
            return EnumCamera.OfficeView

    @property
    def is_door_closed(self) -> Dict[str, bool]:
        # door no use device or not moving
        return {
            "left": 1 - (1 - self.state[0]) * (1 - self.state[6]),
            "right": 1 - (1 - self.state[1]) * (1 - self.state[7])
        }

    @property
    def is_light_on(self) -> Dict[str, bool]:
        return {"left": self.state[2], "right": self.state[3]}

    @property
    def is_monitor_on(self) -> bool:
        return 1 - (1 - self.state[4]) * (1 - self.state[8])

    @property
    def power_remaining(self) -> int:
        return self.state[5]

    @property
    def device_used(self) -> int:
        return np.sum(self.state[:4])

    def update(self, obs_list: List[FreddyEvent], timer):
        # check whether power is used up
        if self.power_remaining == 0:
            if not self.no_power_is_set:
                self.no_power_is_set = True
                for position in self.door_event:
                    if self.door_event[position] is not None:
                        self.door_event[position].set_to_end(finish=False)
                for position in self.light_event:
                    if self.light_event[position] is not None:
                        self.light_event[position].set_to_end(finish=False)
                if self.monitor_event is not None:
                    self.monitor_event.set_to_end(finish=False)
                self._door_open_end("left")
                self._door_open_end("right")
                self._monitor_down_end()
                self._light_end("left")
                self._light_end("right")
                hint_event = HintEvent(message="power used up.")
                self._event_factory.add_event(hint_event)
                self.send_event(hint_event)
            self.to_send_obs = True
        else:
            # if still have power,
            # resond upon player action
            for event in obs_list:
                if event.event_type == FreddyEventType.playerActionEvent:
                    assert isinstance(event, PlayerActionEvent)
                    action = event.action
                    if isinstance(action, PressButtonAction):
                        if action.button == EnumButton.leftDoor:
                            pass
                        elif action.button == EnumButton.rightDoor:
                            pass
                    # produce device movement event
            # if light off or light on:
            # send light off event
            # light off is successor of light on
            # if light on, send observe event to ...
            pass
        # TODO: recalculate device usage

        # if perspective is changed or the game started,
        # renew observation event and send to env
        if self.to_send_obs:
            if self.current_obs_event is not None:
                self.current_obs_event.set_to_end(finish=True)
            self.current_obs_event = ObserveEvent(self.current_view)
            self._event_factory.add_event(self.current_obs_event)
            self.send_event(self.current_obs_event)
        # state event should be at last
        info_event = OfficeInfoEvent(self.state)
        self._event_factory.add_event(info_event)
        self.send_event(info_event)

    # def produce movement event:
    # create movement event
    # create hint event

    # def change state
    # self.current_camera_name = ...
    # self.to_change_view = True

    def _door_close_end(self, position: Literal["left", "right"]):
        hint_event = HintEvent(message="{} door closed.".format(position))
        if position == "left":
            self.state[0] = 1
            self.state[6] = 0
        elif position == "right":
            self.state[1] = 1
            self.state[7] = 0
        else:
            raise ValueError(
                "expect position to be `left` or `right`, \
                    got {}".format(position)
                 )
        self._event_factory.add_event(hint_event)
        self.send_event(hint_event)
        self.to_send_obs = True

    def _door_close_start(self, position: Literal["left", "right"]):
        hint_event = HintEvent(message="closing {} door ..".format(position))
        if position == "left":
            self.state[0] = 1
            self.state[6] = 1
        elif position == "right":
            self.state[1] = 1
            self.state[7] = 1
        if self.door_event[position] is not None:
            assert self.door_event[position].movement == "up"
            self.door_event[position].set_to_end(finish=False)
        door_closing_event = DeviceMovementEvent(
            lifetime_total=door_movement_time,
            device="{} door".format(position),
            movement="down"
        )
        door_closing_event.set_end_func(
            lambda finished:
            self._door_close_end(position) if finished else []
        )
        self.door_event[position] = door_closing_event
        self._event_factory.add_event(hint_event)
        self._event_factory.add_event(door_closing_event)
        self.send_event(hint_event)

    def _door_open_end(self, position: Literal["left", "right"]):
        hint_event = HintEvent(message="{} door opened.".format(position))
        if position == "left":
            self.state[0] = 0
            self.state[6] = 0
        elif position == "right":
            self.state[1] = 0
            self.state[7] = 0
        else:
            raise ValueError(
                "expect position to be `left` or `right`, \
                    got {}".format(position)
                  )
        self._event_factory.add_event(hint_event)
        self.send_event(hint_event)

    def _door_open_start(self, position: Literal["left", "right"]):
        hint_event = HintEvent(message="opening {} door ..".format(position))
        if position == "left":
            self.state[0] = 1
            self.state[6] = 1
        elif position == "right":
            self.state[1] = 1
            self.state[7] = 1
        if self.door_event[position] is not None:
            assert self.door_event[position].movement == "down"
            self.door_event[position].set_to_end(finish=False)
        door_opening_event = DeviceMovementEvent(
            lifetime_total=door_movement_time,
            device="{} door".format(position),
            movement="up"
        )
        door_opening_event.set_end_func(
            lambda finished:
            self._door_open_end(position) if finished else []
        )
        self.door_event[position] = door_opening_event
        self._event_factory.add_event(hint_event)
        self._event_factory.add_event(door_opening_event)
        self.send_event(hint_event)
        self.to_send_obs = True

    def _monitor_up_end(self):
        pass

    def _monitor_up_start(self):
        pass

    def _monitor_down_end(self):
        pass

    def _monitor_down_start(self):
        pass

    def _light_end(self, position:Literal["left", "right"]):
        pass

    def refresh_event_buffer(self):
        super().refresh_event_buffer()
        for pos in self.door_event:
            if self.door_event[pos] is not None and \
                    not self.door_event[pos].is_alive:
                self.door_event[pos] = None
        if self.monitor_event is not None and \
                not self.monitor_event.is_alive:
            self.monitor_event = None
        for pos in self.light_event:
            if self.light_event[pos] is not None and \
                    not self.light_event[pos].is_alive:
                self.light_event[pos] = None


class PirateCove(Room):
    def __init__(self):
        super().__init__(name="PirateCove", locations=["default"])
        self.states = ["hiding", "peering", "to escape"]  # FIXME
        self.state_here = "hiding"
