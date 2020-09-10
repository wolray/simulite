import logging
import time
from typing import List

from simulite.router import *


class Simulation:
    def __init__(self):
        self.event_bus = EventBus()
        self.starters: List[Starter] = []
        self.duration: Optional[int] = None

    def add_starter(self, starter: Starter):
        starter.priority = len(self.starters)
        starter.event_bus = self.event_bus
        self.starters.append(starter)

    def run(self, start_time: Optional[datetime] = None, max_seconds=-1):
        tic = time.time()
        for starter in self.starters:
            starter.before()
            st = starter.start_time or start_time
            if st is not None:
                starter.push(st, starter)
        for _ in self.event_bus.run():
            if 0 < max_seconds < time.time() - tic:
                logging.warning(f'simulation timeout over {max_seconds}s')
                self.event_bus.close()
                break
        for starter in self.starters:
            starter.after()
        self.duration = time.time() - tic
