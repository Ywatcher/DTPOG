from environment import Environment

class Game:
    def __init__(self) -> None:
        self.environment = Environment()
        self.environment.init_set_up_instances()

    @classmethod
    def is_game_over(self) -> bool:
        pass

    def run(self):
        while not self.is_game_over:
            self.environment.update()
