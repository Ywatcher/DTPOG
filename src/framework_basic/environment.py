from collections import Iterable
from typing import List, Dict

from framework_basic.game_object import GameObject
from util.observer import Observer
from framework_basic.event import Event, EventManager


class Environment(Observer):
    def __init__(self) -> None:
        self.concept_domains: Dict[str, type] = {}
        self.instances: Dict[str, List[GameObject]]
        self.event_manager = EventManager()
        self.event_factory = self.event_manager.event_factory
        self.timer = None  # FIXME

    def init_set_up_instances(self):
        for domain in self.concept_domains:
            for instance in self.instances[domain]:
                instance.add_observer(self)
                instance.set_event_factory(self.event_factory)

    @classmethod
    def convert_event(cls, event: Event) -> Dict[GameObject, Iterable[Event]]:
        pass

    def update_as_observer(self, event: Event):
        receiver_message_info = self.convert_event(event)
        for receiver in receiver_message_info.keys():
            messages_to_receiver = receiver_message_info[receiver]
            receiver.receive_message(messages_to_receiver)

    def update(self):
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
