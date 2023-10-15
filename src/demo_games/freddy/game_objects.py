from queue import Queue
import numpy as np
from typing import List, Dict, Optional, Tuple, Iterable, TypedDict
from demo_games.freddy.actions import Action, FreddyQuitAction, PressButtonAction, SelectCameraAction
from demo_games.freddy.cmd_interface import FreddyCmdInterface
from framework_basic.event import Event
from demo_games.freddy.events import CharacterObservedEvent, FreddyEventFactory, FreddyEventMangager, FreddyEventType, MoveEvent, ObserveEvent, PlayerActionEvent
from framework_basic.game_object import GameObject
from framework_basic.environment import Environment
from demo_games.freddy.enums import EnumAction, EnumCamera
from demo_games.freddy.character import *
from demo_games.freddy.rooms import Room, Office


class Player(GameObject):
    def __init__(self, interface: FreddyCmdInterface) -> None:
        super().__init__()
        self._event_factory: FreddyEventFactory = None
        self.interface = interface

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


class _InstanceDict(TypedDict):
    character: List[Character]
    room: List[Room]
    player: List[Player]


class FreddyEnvironment(Environment):
    def __init__(self, interface: FreddyCmdInterface) -> None:
        super().__init__(FreddyEventMangager())
        self.concept_domains = {
            "character": Character, "room": Room, "player": Player}
        self.interface = interface
        self._init_instances()
        self._map_dict = {}
        self._current_room_observated: EnumCamera = EnumCamera.OfficeView
        self._current_player_observation_event: ObserveEvent = None
        self.init_set_up_instances()

    def _init_instances(self):
        self.instances: _InstanceDict = {
            "character": [
                Bonnie(), Freddy(), Chica(), Foxy()
            ],
            "room": [
                Room(name="ShowStage"),
                Room(name="DiningArea", locations=["far", "close", "default"]),
                Room(
                    name="PirateCove",
                    locations=[
                        "hiding",
                        "peering",
                        "escaped"]),
                Room(name="WestHallA"),
                Room(name="WestHallB"),
                Room(name="EastHallA", locations=["far", "close"]),
                Room(name="Backstage", locations=["far", "mid", "close"]),
                Room(name="Kitchen"),
                Room(name="Restrooms", locations=["far", "close"]),  # FIXME
                Office()
            ],
            "player": [Player(self.interface)]
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
            assert isinstance(event, PlayerActionEvent)
            if isinstance(event.action, PressButtonAction):
                # TODO: if press monitor button, switch current view and
                # current obs, if current door open, send to hall
                #
                pass
            elif isinstance(event.action, SelectCameraAction):
                # parse
                cam_name = event.action.camera_name
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
            elif isinstance(event.action, FreddyQuitAction):
                self.game_end = True
                return {}
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
