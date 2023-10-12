from enum import Enum
import re


class EventType(Enum):
    observeEvent = 0


class Event:
    def __init__(self, event_type: EventType) -> None:
        self._event_type = event_type

    @property
    def event_type(self) -> EventType:
        return self._event_type


class ObserveEvent(Event):
    def __init__(self) -> None:
        super().__init__(EventType.observeEvent)
        # TODO: other information
