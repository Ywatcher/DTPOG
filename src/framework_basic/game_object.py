from typing import List, Union
from util.observer import ObservedSubject
from collections.abc import Iterable
from framework_basic.event import Event, EventFactory


class GameObject(ObservedSubject):
    def __init__(self) -> None:
        super().__init__()
        self._received_event_buffer_old = []
        self._received_event_buffer_new = []
        self._event_factory: EventFactory = None

    def set_event_factory(self, event_factory: EventFactory):
        self._event_factory = event_factory

    @classmethod
    def update(cls, event_obs: List[Event], timer):
        # TODO: interpret event as dict
        pass

    def call_update(self, timer):
        # use old event buffer to update
        self.update(self._received_event_buffer_old, timer)

    def refresh_event_buffer(self):
        # remove all dead event and
        # put new event into it
        self._received_event_buffer_old = [
            e
            for e in self._received_event_buffer_old
            if e.is_alive
        ] + self._received_event_buffer_new
        self._received_event_buffer_new = []

    def receive_message(self, m: Iterable[Event]):
        self._received_event_buffer_new += list(m)
