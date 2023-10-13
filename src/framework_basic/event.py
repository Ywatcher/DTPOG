from abc import ABC
from enum import Enum
from typing import List


class EventType(Enum):
    pass


class Event(ABC):
    def __init__(self, event_type: EventType, lifetime_total: int) -> None:
        self._event_type = event_type
        self.lifetime_total = lifetime_total
        self.life_current = lifetime_total + 1

    @property
    def event_type(self) -> EventType:
        return self._event_type

    def reduce_life(self):
        self.life_current -= 1

    @property
    def is_alive(self) -> bool:
        return self.life_current > 0

    @classmethod
    def end(cls) -> List["Event"]:
        # return successor events
        pass


class EventFactory:
    def __init__(self, event_manager: "EventManager") -> None:
        self.event_manager = event_manager


class EventManager:
    def __init__(self) -> None:
        self._all_events = []

    @property
    def event_factory(self) -> EventFactory:
        pass

    def add_event(self, event: Event):
        self._all_events.append(event)

    def reduce_life_all(self) -> List[Event]:
        successors = []
        for event in self._all_events:
            assert event.is_alive
            event.reduce_life()
            if not event.is_alive:
                successors_of_this = event.end()
                successors += successors_of_this
        for event in successors:
            assert event.is_alive
            event.reduce_life()
        return successors

    def delete_dead_event(self):
        dead_events = [e for e in self._all_events if not e.is_alive]
        self._all_events = [e for e in self._all_events if e.is_alive]
        for e in dead_events:
            del e
