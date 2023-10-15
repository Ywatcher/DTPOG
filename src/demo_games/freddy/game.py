from demo_games.freddy.game_objects import FreddyEnvironment


if __name__ == "__main__":
    e = FreddyEnvironment()
    nr_iter = 10
    while nr_iter > 0:
        e.update()
        nr_iter -= 1
