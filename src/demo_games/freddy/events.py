from enum import Enum
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
    # monitorEvent = 12
    lightDurationEvent = 13
    currentViewEvent = 14


FreddyEvent = Event[FreddyEventType]
# FIXME
knock_door_time = 600
light_duration = 500


class ObserveEvent(StaticEvent[FreddyEventType]):
    def __init__(self, camera_name: EnumCamera) -> None:
        super().__init__(FreddyEventType.observeEvent)
        # TODO: other information
        self.camera_name = camera_name

    def end(self):
        return []


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
                 office_state: np.ndarray,
                 current_view:EnumCamera) -> None:
        super().__init__(FreddyEventType.officeInfoEvent, lifetime_total=1)
        # TODO: use static event instead
        # now: event with lifetime 1
        self.office_state = office_state
        self.current_view = current_view

    def __repr__(self) -> str:
        return "{}: {}".format(self.event_type.name, self.office_state)


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

    def __repr__(self) -> str:
        return "Event: {} {}".format(
            self.device, self.movement
        )


class LightDurationEvent(FreddyEvent):
    # during duration, the light is on
    def __init__(self) -> None:
        super().__init__(
            FreddyEventType.lightDurationEvent,
            light_duration
        )

    def renew(self):
        self.life_current = self.lifetime_total


class HintEvent(FreddyEvent):
    def __init__(self, message: str) -> None:
        super().__init__(FreddyEventType.hintEvent, 1)
        self.message = message  # FIXME: for cmd only, what if gui?

class FreddyEventManager(EventManager[FreddyEvent]):

    def __init__(self) -> None:
        super().__init__()
        self._event_factory: EventFactory[FreddyEvent] = EventFactory(self)

    @property
    def event_factory(self) -> EventFactory[FreddyEvent]:
        return self._event_factory
