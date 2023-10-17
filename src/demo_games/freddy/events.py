from enum import Enum
import re
from sys import call_tracing
from typing import Callable, List, Literal, Tuple, Union
from demo_games.freddy.actions import Action
from framework_basic.event import Event, EventFactory, EventManager, StaticEvent
from demo_games.freddy.enums import EnumCamera, EnumAction, EnumButton
import numpy as np


class FreddyEventType(Enum):
    observeEvent = 0  # from env to character
    moveEvent = 1  # from character to env
    jumpScareEvent = 2  # from character to env to player
    characterObservedEvent = 4  # from character to env to player
    hitDoorEvent = 5  # from character to env to player
    foxyRunEvent = 6  # from character to env to player
    playerActionEvent = 7  # from player to env
    officeInfoEvent = 8  # from office to env to player and all character
    # office to player, produce with start hint at same time, and itself
    # produce end hint
    deviceMovementEvent = 10
    hintEvent = 11  # from anything to player


FreddyEvent = Event[FreddyEventType]


class ObserveEvent(StaticEvent[FreddyEventType]):
    def __init__(self, camera_name: EnumCamera) -> None:
        super().__init__(FreddyEventType.observeEvent)
        # TODO: other information
        self.camera_name = camera_name

    def end(self):
        return []


# FIXME
knock_door_time = 6


class HitDoorEvent(Event[FreddyEventType]):
    def __init__(self, character: str) -> None:
        super().__init__(FreddyEventType.hitDoorEvent, knock_door_time)
        self.character = character


class MoveEvent(Event[FreddyEventType]):
    def __init__(
        self,
        character: str,
        from_: Tuple[str, str],
        to_: Tuple[str, str],
        lifetime_total: int = 1
    ) -> None:
        super().__init__(FreddyEventType.moveEvent, lifetime_total)
        self.character = character
        self.from_ = from_
        self.to_ = to_


class PlayerActionEvent(Event[FreddyEventType]):
    # select monitor + camera_name
    #  -> create obs event
    #  -> disable previous obs event
    # monitor up
    # -> as previous monitor
    # monitor down
    # as office view
    # if office is observed, send office state to player
    # left door button
    # send to office
    def __init__(self, action: Action) -> None:
        super().__init__(FreddyEventType.playerActionEvent, 1)
        self.action = action


class CharacterObservedEvent(Event[FreddyEventType]):
    def __init__(self, character, location: Tuple[str, str]) -> None:
        super().__init__(FreddyEventType.characterObservedEvent, 1)
        self.character = character
        self.location = location

    def __repr__(self) -> str:
        return "{}:{} at {}".format(
            self.event_type.name,
            self.character,
            self.location
        )


class JumpScareEvent(Event[FreddyEventType]):
    def __init__(
        self,
        character: str,
        lifetime_total: int
    ) -> None:
        super().__init__(FreddyEventType.jumpScareEvent, lifetime_total)
        self.character = character

    def end(self):
        # TODO: game finish
        pass


class FoxyRunEvent(Event[FreddyEventType]):
    def __init__(self) -> None:
        super().__init__(FreddyEventType.foxyRunEvent, 30)


class OfficeInfoEvent(Event[FreddyEventType]):
    def __init__(self,
                 office_state: np.ndarray) -> None:
        super().__init__(FreddyEventType.officeInfoEvent, lifetime_total=1)
        # TODO: use static event instead
        # now: event with lifetime 1
        self.office_state = office_state

    def __repr__(self) -> str:
        return "{}: {}".format(self.event_type.name, self.office_state)


class FreddyEventManager(EventManager[FreddyEvent]):

    def __init__(self) -> None:
        super().__init__()
        self._event_factory: EventFactory[FreddyEvent] = EventFactory(self)

    @property
    def event_factory(self) -> EventFactory[FreddyEvent]:
        return self._event_factory


class DeviceMovementEvent(FreddyEvent):
    def __init__(
        self, lifetime_total: int,
        device: str,  # FIXME
        movement: Literal["up", "down"]
    ) -> None:
        super().__init__(
            FreddyEventType.deviceMovementEvent,
            lifetime_total
        )
        self.device = device
        self.movement = movement
        self.funclist: List[Callable] = []

    def __repr__(self) -> str:
        return "Event: {} {}".format(
            self.device, self.movement
        )

    def set_end_func(self, end_func: Callable):
        self.funclist.append(end_func)  # todo: add order

    def end(self) -> List[FreddyEvent]:
        successors = []
        for func in self.funclist:
            result = func()
            if result is not None:
                if isinstance(result, Event):
                    successors.append(result)
                elif isinstance(result, list):
                    successors.append(result)
                else:
                    assert False, \
                        "result should be either event or list, got {}".format(
                            type(result)
                        )
        return successors

    # TODO:
    # hook start and end; done

# TODO: create these events in office
#

# TODO: move to event factory


class MonitorEvent(FreddyEvent):
    # monitor already set on or off
    # if monitor on, env send camera obs to room and character
    # loop 0 - 1
    # monitor_on_movement.end()
    # loop 0 - 2
    # -> set office state
    # generate successor -> env send cam obs
    # -> hint event: monitor down. to character
    # loop 0 - 1
    # update, send obs to you
    pass


class HintEvent(FreddyEvent):
    def __init__(self, message: str) -> None:
        super().__init__(FreddyEventType.hintEvent, 1)
        self.message = message  # FIXME: for cmd only, what if gui?


class LightDurationEvent(FreddyEvent):
    # during duration, the light is on
    # send to no one
    pass

    # end:
    # inform office to turn off light
    # and a hint: light off if no another LightDurationEvent in obs list for
    # office
    # how to judge?
    # for office,  it should have a list
    # duration events that exisr
    # lighton() -> if not duration events: create one
    # else: renew one
    def renew(self):
        # self.life = lifetime_total
        pass

    # if


# for door, the problem is,
# that the door is considered as open during movement
# but it uses power

# for office :
# self.left_door_event = ...
# if pressed door button when left_door_event is opening
# end it as unfinished
# and create a new one : closing
#


# calculate power :
# if closed in state vector: as closed
# for character: open if closing / opening
# or open in state vector
# the last two dim of vector as left opening / right opening
# for door duration event:
