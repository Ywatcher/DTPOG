from queue import Queue
import numpy as np
from typing import List, Dict, Optional, Tuple, Iterable, TypedDict
from demo_games.freddy.actions import Action, PressButtonAction, SelectCameraAction
from framework_basic.event import Event
from demo_games.freddy.events import CharacterObservedEvent, FreddyEventFactory, FreddyEventType, MoveEvent, ObserveEvent
from framework_basic.game_object import GameObject
from framework_basic.environment import Environment
from demo_games.freddy.enums import EnumAction, EnumCamera
from demo_games.freddy.character import *


class Room(GameObject):
    def __init__(
            self, name: str,
            locations: Optional[List[str]] = None) -> None:
        super().__init__()
        self.name = name
        if locations is not None:
            self.locations = locations
        else:
            self.locations = ["default"]


class Player(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self._event_factory: FreddyEventFactory = None
        from demo_games.freddy.cmd_interface import FreddyCmdInterface
        self.interface = FreddyCmdInterface()

    def receive_message(self, m: List[Event]):
        return super().receive_message(m)

    def update(self, obs_list: List[Event], timer):
        # do not show the list of event since
        # it has been showed when received
        self.interface.update_obs(obs_list)
        a: Action = self.interface.get_input()  # get all
        if a is not None:
            e = self._event_factory.produce_action_event(a)
            self.send_event(e)


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
        return {"left": self.state[1], "right": self.state[2]}

    @property
    def is_monitor_on(self) -> bool:
        return self.state[3]

    @property
    def power_remaining(self) -> int:
        return self.state[4]

    @property
    def device_used(self) -> int:
        return np.sum(self.state[:4])

    def update(self, obs_list: List[Event]):
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


class PirateCove(Room):
    def __init__(self):
        super().__init__(name="PirateCove", locations=["default"])
        self.states = ["hiding", "peering", "to escape"]  # FIXME
        self.state_here = "hiding"


class _InstanceDict(TypedDict):
    character: List[Character]
    room: List[Room]
    player: List[Player]


class FreddyEnvironment(Environment):
    def __init__(self) -> None:
        super().__init__()
        self.concept_domains = {
            "character": Character, "room": Room, "player": Player}
        self._init_instances()
        self._map_dict = {}
        self._current_room_observated: EnumCamera = EnumCamera.OfficeView
        self._current_player_observation_event: ObserveEvent = None

    def init_set_up_instances(self):
        print("called")
        return super().init_set_up_instances()

    def _init_instances(self):
        self.instances: _InstanceDict = {
            "character": [
                Bonnie(), Freddy(), Chica(), Foxy()
            ],
            "room": [
                Room(name="ShowStage"),
                Room(name="DiningArea", locations=["far", "close", "default"]),
                PirateCove(),
                Room(name="WestHallA"),
                Room(name="WestHallB"),
                Room(name="EastHallA", locations=["far", "close"]),
                Room(name="Backstage", locations=["far", "mid", "close"]),
                Room(name="Kitchen"),
                Room(name="Restrooms", locations=["far", "close"]),  # FIXME
                Office()
            ],
            "player": [Player()]
        }
        self._map_dict = {
            "character": {
                c.name: c
                for c in self.instances["character"]
            },
            "room": {
                r.name: r
                for r in self.instances["room"]
            }
        }

    @property
    def get_player(self) -> Player:
        return self.instances["player"][0]

    def get_room(self, room_name: str) -> Room:
        return self._map_dict["room"][room_name]

    def convert_event(self, event: Event) -> Dict[GameObject, Iterable[Event]]:
        # if event.event_type == FreddyEventType.observeEvent:
        if event.event_type == FreddyEventType.playerActionEvent:
            # produce observation event
            # send produced event to charactes observed
            from demo_games.freddy.events import ObserveEvent
            if isinstance(event, PressButtonAction):
                # TODO: if press monitor button, switch current view and
                # current obs, if current door open, send to hall
                #
                pass
            elif isinstance(event, SelectCameraAction):
                # parse
                cam_name = event.camera_name
                room_to_see = cam_name.room()
                characters_you_can_see = [
                    c for c in self.instances["character"]
                    if c.location[0] == room_to_see
                ]
                objects_observed = characters_you_can_see \
                    + [self.get_room(room_to_see)]
                self._current_player_observation_event.set_to_end()
                # send
                new_observation_event = ObserveEvent(cam_name)
                self._current_player_observation_event = new_observation_event
                return {
                    obj: [new_observation_event]
                    for obj in objects_observed
                }
        elif event.event_type == FreddyEventType.characterObservedEvent:
            # send to player
            return {self.get_player: [event]}
#         elif event.event_type == FreddyEventType.jumpScareEvent:
        elif event.event_type == FreddyEventType.moveEvent:
            # parse
            assert isinstance(event, MoveEvent)
            destination = event.to_
            # for characters that reached office door, left or right,
            # tell them whether the door is open
            if destination[0] == "Office":
                pass
            if destination[0] == \
                    self._current_player_observation_event.camera_name.room():
                # send
                e = CharacterObservedEvent(
                    character=event.character,
                    location=destination
                )
                self.event_factory.add_event(e)
                return {self.get_player: [event]}
            else:
                # send nothing
                return {}
        else:
            raise ValueError
            pass
