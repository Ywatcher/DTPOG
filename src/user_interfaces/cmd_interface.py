from queue import Queue
from threading import Thread, Lock
from abc import ABC
from typing import List
from framework_basic.event import Event


class InputParsesr(ABC):
    class _TerminateAction:
        def __eq__(self, __value: object) -> bool:
            return isinstance(__value, InputParsesr._TerminateAction)

    def __init__(self) -> None:
        self._terminateAction = InputParsesr._TerminateAction()

    @property
    def TerminateAction(self) -> "InputParsesr._TerminateAction":
        return self._terminateAction

    @classmethod
    def parse(cls, s: str) -> object:
        pass


class CMDInterface(ABC):
    def __init__(self, input_parser: InputParsesr) -> None:
        self.queue = Queue()
        self.thread = Thread(
            target=self.listen_input
        )
        self.input_parser = input_parser
        self.lock = Lock()
        # TODO: a boolean flag to indicate whether the thread
        # is started

    def listen_input(self):
        while True:
            input_str = input()
            self.lock.acquire()
            parsed_input_obj = self.input_parser.parse(input_str)
            self.lock.release()
            if parsed_input_obj is not None:
                if self.input_parser.TerminateAction != parsed_input_obj:
                    self.queue.put(input_str)
                else:
                    break

    def start(self):
        self.thread.start()

    def get_input(self):
        # TODO use try
        if not self.queue.empty():
            return self.queue.get(False)
        return None

    @classmethod
    def update_obs(cls, obs_list: List[Event]):
        pass
