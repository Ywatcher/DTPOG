from collections import Iterable
from typing import List, Dict

from framework.game_object import GameObject
from util.observer import Observer
from event import Event, EventManager


class Environment(Observer):
    def __init__(self) -> None:
        self.concept_domains: Dict[str, type] = {}
        self.instances: Dict[str, List[GameObject]]
        self.event_manager = EventManager()
    @classmethod
    def convert_event(cls, event: Event) -> Dict[GameObject, Iterable[Event]]:
        pass

    def update_as_observer(self, event: Event):
        receiver_message_info = self.convert_event(event)
        for receiver in receiver_message_info.keys():
            messages_to_receiver = receiver_message_info[receiver]
            receiver.receive_message(messages_to_receiver)

    def update(self):
        for domain in self.instances.keys():
            for instance in self.instances[domain]:
                instance.call_update()
        self.event_manager.reduce_life_all()
        for domain in self.instances.keys():
            for instance in self.instances[domain]:
                instance.refresh_event_buffer()
        self.event_manager.delete_dead_event()
