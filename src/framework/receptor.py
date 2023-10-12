from util.observer import ObservedSubject


class Receptor(ObservedSubject):
    def __init__(self) -> None:
        self._obs = {}  # empty obs
        self._is_on = False

    def set_obs(self, obs: dict):
        self._obs = obs.copy()

    def update_obs_buffer(self, obs: dict):
        self._obs.update(obs)

    @property
    def obs(self) -> dict:
        return self._obs.copy()

    def clear(self):
        self._obs = {}

    def on(self):
        self._is_on = True

    def off(self):
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    def send_observe_message(self):
        event = None
        self.send_event(event)
