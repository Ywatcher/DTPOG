from framework.event import Event, EventType


class DemoEventType(EventType):
    observeEvent = 0


class ObserveEvent(Event):
    def __init__(self) -> None:
        super().__init__(DemoEventType.observeEvent, lifetime_total=1)
        # TODO: other information
