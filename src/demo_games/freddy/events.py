from sys import call_tracing
from typing import Tuple, Union
from demo_games.freddy.actions import Action
from framework_basic.event import Event, EventFactory, EventType, StaticEvent
from demo_games.freddy.enums import EnumCamera, EnumAction, EnumButton


class FreddyEventType(EventType):
    observeEvent = 0
    moveEvent = 1
    jumpScareEvent = 2
    characterObservedEvent = 4
    hitDoorEvent = 5
    foxyRunEvent = 6
    playerActionEvent = 7


class ObserveEvent(StaticEvent):
    def __init__(self, camera_name: EnumCamera) -> None:
        super().__init__(FreddyEventType.observeEvent)
        # TODO: other information
        self.camera_name = camera_name

    def end(self):
        return []


class KnockDoorEvent(Event):
    pass


class MoveEvent(Event):
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


class PlayerActionEvent(Event):
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


class CharacterObservedEvent(Event):
    def __init__(self, character, location: Tuple[str, str]) -> None:
        super().__init__(FreddyEventType.characterObservedEvent, 1)
        self.info = character = character
        self.location = location


class JumpScareEvent(Event):
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


class FoxyRunEvent(Event):
    def __init__(self) -> None:
        super().__init__(FreddyEventType.foxyRunEvent, 30)


class FreddyEventFactory(EventFactory):
    def produce_jump_scare_event(self, character: str) -> JumpScareEvent:
        pass

    def produce_knock_door_event(self, character: str) -> KnockDoorEvent:
        pass

    def produce_action_event(
            self,
            action: Action) -> PlayerActionEvent:
        e = PlayerActionEvent(action)
        self.event_manager.add_event(e)
        return e
