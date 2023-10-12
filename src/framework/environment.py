from collections import Iterable
from typing import List, Dict

from framework.game_object import GameObject
from framework.receptor import Receptor
from util.observer import Observer
from event import Event


class Environment(Observer):
    def __init__(self) -> None:
        self.concept_domains: Dict[str, type] = {}
        self.perspectives: List[Receptor] = []
        self.instances: Dict[str, List[GameObject]]

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
                instance.update_send_message()
        for perspective in self.perspectives:
            if perspective.is_on:
                perspective.send_observe_message()
        # TODO: set obs

        for domain in self.instances.keys():
            for instance in self.instances[domain]:
                instance.refresh_event_buffer()
