import logging
import time
from typing import List

from router import *


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
        while self.event_bus.pop():
            if 0 < max_seconds < time.time() - tic:
                logging.warning(f'timeout limit ({max_seconds}s) exceeded')
                break
        for starter in self.starters:
            starter.after()
        self.duration = time.time() - tic
