from framework_basic.environment import Environment


class Game:
    def __init__(self) -> None:
        self.environment = Environment()
        self.environment.init_set_up_instances()
        self.nr_iter = 0

    @property
    def is_game_over(self) -> bool:
        return self.nr_iter < 10

    def run(self):
        while not self.is_game_over:
            self.environment.update()
            self.nr_iter += 1


if __name__ == "__main__":
    game = Game()
    game.run()
