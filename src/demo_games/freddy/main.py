from demo_games.freddy.cmd_interface import FreddyCmdInterface
from demo_games.freddy.game_objects import FreddyEnvironment
import time

if __name__ == "__main__":
    interface = FreddyCmdInterface()
    e = FreddyEnvironment(interface)
    interface.start()
    try:
        while not e.game_end:
            e.update()
            time.sleep(1e-2)  # each frame: 10 ms
    finally:
        interface.join()
