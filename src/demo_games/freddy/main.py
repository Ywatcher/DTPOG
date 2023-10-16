from demo_games.freddy.cmd_interface import FreddyCmdInterface
from demo_games.freddy.game_objects import FreddyEnvironment


if __name__ == "__main__":
    interface = FreddyCmdInterface()
    e = FreddyEnvironment(interface)
    print("u0")
    # e.update()
    interface.start()
    try:
        while not e.game_end:
            e.update()
    finally:
        interface.join()
