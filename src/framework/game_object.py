from util.observer import ObservedSubject
from collections.abc import Iterable


class GameObject(ObservedSubject):
    def __init__(self) -> None:
        super().__init__()
        self._received_event_buffer_old = []
        self._received_event_buffer_new = []

    @classmethod
    def update(cls, event_obs: list):
        # TODO: interpret event as dict
        pass

    def call_update(self):
        # use old event buffer to update
        self.update(self._received_event_buffer_old)

    def refresh_event_buffer(self):
        self._received_event_buffer_old = self._received_event_buffer_new
        self._received_event_buffer_new = []

    def receive_message(self, m):
        if isinstance(m, Iterable):
            self._received_event_buffer_new += list(m)
        else:
            self._received_event_buffer_new.append(m)
