from typing import List, Dict
from framework.game_object import GameObject
from framework.environment import Environment


class Character(GameObject):
    pass


class Room(GameObject):
    pass


class Freddy(Character):
    def update(self):
        if observed:
            self.state = None
        else:
            self.state = None

    pass


class Kitchen(Room):
    pass


class FreddyEnvironment(Environment):
    def __init__(self) -> None:
        super().__init__()
        self.concept_domains = {"character": Character, "room": Room}
        self.init_instances()
        # todo:
        # bind receptors with instances

    def init_instances(self):
        self.perspectives = []
        self.instances: Dict[str, List[GameObject]] = {
            "character": [], "room": []}
