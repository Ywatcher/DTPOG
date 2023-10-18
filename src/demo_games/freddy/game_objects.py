from typing import List, Dict, Optional, Tuple, Iterable, TypedDict
from demo_games.freddy.actions import Action, FreddyQuitAction, \
    PressButtonAction, SelectCameraAction
from demo_games.freddy.cmd_interface import FreddyCmdInterface
from framework_basic.event import Event, EventFactory, EventManager
from demo_games.freddy.events import *
from framework_basic.game_object import GameObject
from framework_basic.environment import Environment
from demo_games.freddy.enums import EnumAction, EnumButton, EnumCamera
from demo_games.freddy.character import *
from demo_games.freddy.rooms import Room, Office


class Player(GameObject[FreddyEvent]):
    def __init__(self, interface: FreddyCmdInterface) -> None:
        super().__init__()
        self.interface = interface

    def receive_message(self, m: List[FreddyEvent]):
        return super().receive_message(m)

    def update(self, obs_list: List[FreddyEvent], timer):
        self.interface.update_obs(obs_list)
        a: Action = self.interface.get_input()  # get all
        if a is not None:
            e = PlayerActionEvent(a)
            self._event_factory.add_event(e)
            self.send_event(e)


class _InstanceDict(TypedDict):
    character: List[Character]
    room: List[Room]
    player: List[Player]


class FreddyEnvironment(Environment):
    def __init__(self, interface: FreddyCmdInterface) -> None:
        super().__init__(FreddyEventManager())
        self.concept_domains = {
            "character": Character, "room": Room, "player": Player}
        self.interface = interface
        self._init_instances()
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
                        "to_escape"]),
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

    @property
    def get_office(self) -> Office:
        return self.get_room("Office")

    def get_room(self, room_name: str) -> Room:
        return self._map_dict["room"][room_name]

    def convert_event(
        self, event: Event
    ) -> Dict[GameObject[FreddyEvent], Iterable[FreddyEvent]]:

        if event.event_type == FreddyEventType.playerActionEvent:
            # TODO: distinguish game action and game menu action
            assert isinstance(event, PlayerActionEvent)
            # game actions:
            #   send this event to office and let office process this;
            #   then office will produce corresponding observation event
            #   which will be send by office to charactes
            if isinstance(event.action, PressButtonAction) \
                    or isinstance(event.action, SelectCameraAction):
                # send to office;
                # office will set door open and create opening event;
                #   and hint event
                return {self.get_office: [event]}
            # game menu actions:
            elif isinstance(event.action, FreddyQuitAction):
                self.game_end = True
                return {}
        elif event.event_type == FreddyEventType.observeEvent:
            assert isinstance(event, ObserveEvent)
            cam_name = event.camera_name
            room_to_see = cam_name.room()
            characters_you_can_see = [
                c for c in self.instances["character"]
                if c.location[0] == room_to_see
            ]
            objects_observed = characters_you_can_see \
                + [self.get_room(room_to_see)]
            return {
                obj: [event]
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
        elif isinstance(event, OfficeInfoEvent):
            characters_and_player = self.instances["character"] + \
                self.instances["player"]
            return {
                obj: [event]
                for obj in characters_and_player
            }

        else:
            return {}
