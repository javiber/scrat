import time


class Timer:
    "Simple timer."

    def __init__(self) -> None:
        self._start_time = None

    def start(self):
        self._start_time = time.time()

    def end(self) -> float:
        try:
            delta = time.time() - self._start_time
        except TypeError:
            raise RuntimeError("Trying to stop a timer that has not been started")
        self._start_time = None
        return delta
