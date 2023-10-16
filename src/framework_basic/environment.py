from collections import Iterable
from typing import Generic, List, Dict

from framework_basic.game_object import GameObject
from util.observer import Observer
from framework_basic.event import Event, EventManager, event_T


class Environment(Observer, Generic[event_T]):
    def __init__(self, event_manager: EventManager[event_T]) -> None:
        self.concept_domains: Dict[str, type] = {}
        self.instances: Dict[str, List[GameObject]]
        self.event_manager = event_manager
        self.event_factory = self.event_manager.event_factory
        self.timer = None  # FIXME
        self.game_end = False

    def init_set_up_instances(self):
        for domain in self.concept_domains:
            for instance in self.instances[domain]:
                instance.add_observer(self)
                instance.set_event_factory(self.event_factory)

    @classmethod
    def convert_event(
            cls, event: event_T
    ) -> Dict[GameObject[event_T], Iterable[event_T]]:
        raise NotImplementedError

    def update_as_observer(self, event: event_T):
        receiver_message_info = self.convert_event(event)
        for receiver in receiver_message_info.keys():
            messages_to_receiver = receiver_message_info[receiver]
            receiver.receive_message(messages_to_receiver)

    def update(self, *args):
        # each instance reacts upon
        for domain in self.instances.keys():
            for instance in self.instances[domain]:
                instance.call_update(self.timer)

        # previous reduce life
        # FIXME: the order
        # reduce each event's lifetime by 1
        # if an event is about to end, it may
        # triger events that goes after it
        # if no event is trigered, an empty list
        # is produced by this event.
        successor_events = self.event_manager.reduce_life_all()
        for e in successor_events:
            self.update_as_observer(e)

        for domain in self.instances.keys():
            for instance in self.instances[domain]:
                instance.refresh_event_buffer()
        self.event_manager.delete_dead_event()
