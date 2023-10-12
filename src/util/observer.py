from abc import ABC
from typing import List


class Observer(ABC):
    @classmethod
    def update_as_observer(cls, event):
        pass

    def priority(self) -> float:
        pass


class ObservedSubject:
    def __init__(self) -> None:
        # TODO: with priority
        self.observers: List[Observer] = []

    def add_observer(self, o: Observer):
        assert o not in self.observers
        self.observers.append(o)

    def send_event(self, event):
        for o in self.observers:
            o.update_as_observer(event)

    def remove_observer(self, o: Observer):
        self.observers.remove(o)
