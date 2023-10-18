from typing import Callable, TypeVar
from abc import ABC
from enum import Enum
from typing import Generic, List, overload
from util.func import n_args
# from numpy import inf


event_enum_T = TypeVar("event_enum_T", Enum, object)


class Event(ABC, Generic[event_enum_T]):
    def __init__(self, event_type: event_enum_T, lifetime_total: int) -> None:
        self._event_type = event_type
        self.lifetime_total = lifetime_total
        self.life_current = lifetime_total
        self.funclist: List[Callable] = []
        self._is_to_end = False
        self._properly_finish = True

    def set_to_end(self, finish: bool):
        self._is_to_end = True
        self._properly_finish = finish

    @property
    def event_type(self) -> event_enum_T:
        return self._event_type

    def reduce_life(self):
        if self._is_to_end:
            self.life_current = -1
        self.life_current -= 1

    @property
    def is_alive(self) -> bool:
        return self.life_current >= 0

    def set_end_func(self, end_func: Callable):
        self.funclist.append(end_func)  # todo: add order

    def end(self) -> List["Event[event_enum_T]"]:
        finished = self._properly_finish
        successors = []
        for func in self.funclist:
            if n_args(func) == 0:
                result = func()
            else:
                result = func(finished)
            if result is not None:
                if isinstance(result, Event):
                    successors.append(result)
                elif isinstance(result, list):
                    successors.append(result)
                else:
                    assert False, \
                        "result should be either event or list, got {}".format(
                            type(result)
                        )
        return successors


class StaticEvent(Event, Generic[event_enum_T]):
    def __init__(self, event_type: event_enum_T) -> None:
        super().__init__(event_type, lifetime_total=1)

    def reduce_life(self):
        # do not reduce life
        if self._is_to_end:
            self.life_current = -1


event_T = TypeVar("event_T", Event, Event)


class EventFactory(Generic[event_T]):
    def __init__(self, event_manager: "EventManager[event_T]") -> None:
        self.event_manager = event_manager

    def add_event(self, e: event_T):
        self.event_manager.add_event(e)


class EventManager(Generic[event_T]):
    def __init__(self) -> None:
        self._all_events = []

    @property
    def event_factory(self) -> EventFactory[event_T]:
        pass

    def add_event(self, event: event_T):
        self._all_events.append(event)

    def reduce_life_all(self) -> List[event_T]:
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
