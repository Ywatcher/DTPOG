from demo_games.freddy.cmd_interface import FreddyCmdInterface
from demo_games.freddy.game_objects import FreddyEnvironment


if __name__ == "__main__":
    interface = FreddyCmdInterface()
    e = FreddyEnvironment(interface)
    interface.start()
    # n = 10
    try:
        while not e.game_end:
            e.update()
            # n += 1
            # interface.set_prompt("{}".format(n))
    finally:
        interface.join()
