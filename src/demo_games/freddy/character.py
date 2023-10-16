import numpy as np
from typing import List, Dict, Optional, Tuple, Iterable, TypedDict
from framework_basic.event import Event
from demo_games.freddy.events import CharacterObservedEvent, FreddyEvent, FreddyEventType, JumpScareEvent, KnockDoorEvent
from framework_basic.game_object import GameObject


class Character(GameObject):
    def __init__(
        self,
        name: str, tick_period: int,
        location: Tuple[str, str],
        jump_scare_duration=1  # FIXME
    ) -> None:
        super().__init__()
        self.location = location
        self.name = name
        self._state = 0
        self._tick_count = 0  # character's tick within each period
        self._tick_period = tick_period
        self._jump_scare_duration = jump_scare_duration

    @property
    def state(self) -> int:
        return self._state

    def is_observed(self, obs_list: Iterable[FreddyEvent]) -> bool:
        for event in obs_list:
            if event.event_type == FreddyEventType.observeEvent:
                return True
        return False

    def tick(self, obs_list: List[FreddyEvent], timer):
        pass

    def update(self, obs_list: List[FreddyEvent], timer):
        if self._tick_count < self._tick_period:
            self._tick_count += 1
        else:
            self.tick(obs_list, timer)
            self._tick_count = 0
        # print("{} updating".format(self.name))
        if self.is_observed(obs_list):
            observated = CharacterObservedEvent(self.name, self.location)
            self._event_factory.add_event(observated)
            self.send_event(observated)

    def knock_door(self):
        knock_door_event = KnockDoorEvent(character=self.name)
        self._event_factory.add_event(knock_door_event)
        self.send_event(knock_door_event)

    def kill_player(self):
        jump_scare_event = JumpScareEvent(
            character=self.name, lifetime_total=self._jump_scare_duration
        )
        self._event_factory.add_event(jump_scare_event)
        self.send_event(jump_scare_event)


class Bonnie(Character):
    def __init__(self) -> None:
        super().__init__(
            name="Bonnie",
            tick_period=1000,
            location=(
                "ShowStage",
                "default"))


class Chica(Character):
    def __init__(self) -> None:
        super().__init__(
            name="Chica",
            tick_period=1300,
            location=(
                "ShowStage",
                "default"))


class Freddy(Character):
    def __init__(self) -> None:
        super().__init__(
            name="Freddy",
            tick_period=1700,
            location=(
                "ShowStage",
                "default"))

    def update(self, obs_list: List[FreddyEvent], timer):
        super().update(obs_list, timer)


class Foxy(Character):
    def __init__(self) -> None:
        super().__init__(
            name="Foxy", tick_period=1900, location=("PirateCove", "hiding"))
