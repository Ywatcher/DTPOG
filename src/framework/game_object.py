from typing import Dict, List
from util.observer import ObservedSubject
from collections.abc import Iterable


class GameObject(ObservedSubject):
    def __init__(self) -> None:
        super().__init__()
        self._received_event_buffer_old = []
        self, _received_event_buffer_new = []

    @classmethod
    def update(cls):
        # use old event buffer to update
        pass
        # return the obs of last time

    def update_send_message(self):
        pass

    def refresh_event_buffer(self):
        self._received_event_buffer_old = self._received_event_buffer_new
        self._received_event_buffer_new = []

    def receive_message(self, m):
        if isinstance(m, Iterable):
            self._received_event_buffer_new += list(m)
        else:
            self._received_event_buffer_new.append(m)
