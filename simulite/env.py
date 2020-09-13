from __future__ import annotations

import time as timer
from datetime import datetime, timedelta
from queue import PriorityQueue
from typing import *


def merge(*actions: Action) -> Action:
    def new(t):
        for action in actions:
            action(t)

    return new


class Event:
    def __init__(self, time: datetime, priority: int, action: Action):
        self.time = time
        self.key = (time, priority)
        self.action = action

    def prepend(self, action: Action) -> Event:
        self.action = merge(action, self.action)
        return self

    def append(self, action: Action) -> Event:
        self.action = merge(self.action, action)
        return self


class Env:
    def __init__(self):
        self.starters: List[Starter] = []
        self.pq = PriorityQueue()
        self.map: Dict[tuple, Event] = {}
        self.beg: Optional[datetime] = None
        self.now: Optional[datetime] = None
        self.end: Optional[datetime] = None
        self.duration: Optional[int] = None

    def add_starter(self, starter: Starter):
        self.starters.append(starter)

    def push(self, time: datetime, action: Action, prior=0) -> Event:
        """
        push an event onto the queue
        merge if the key is duplicated
        :param time: event time
        :param action: event action
        :param prior: used for sorting events happened in the same time
        :return: pushed event if not merged else the old one
        """
        event = Event(time, prior, action)
        key = event.key
        old = self.map.get(key)
        if old:
            old.append(event.action)
            return old
        else:
            self.pq.put(key)
            self.map[key] = event
            return event

    def run(self, max_seconds=-1):
        tic = timer.time()

        for starter in self.starters:
            starter(self)

        while not self.pq.empty():
            key = self.pq.get()
            event = self.map.pop(key)
            t = event.time
            if self.beg is None:
                self.beg = t
            self.now = t
            event.action(t)
            if 0 < max_seconds < timer.time() - tic:
                import logging
                logging.warning(f'simulation timeout over {max_seconds}s')
                break
        self.end = self.now

        self.duration = timer.time() - tic

    def time_span(self) -> Optional[timedelta]:
        """
        :return: time span between the first and the last events
        """
        return self.end - self.beg if self.end else None

    def repeat(self, start_time: datetime, period: timedelta, action: Action, terminator: Terminator):
        def _repeat(t):
            if not terminator(t):
                action(t)
                self.repeat(t + period, period, action, terminator)

        self.push(start_time, _repeat)
        return self


Action = Callable[[datetime], None]
Starter = Callable[[Env], None]
Terminator = Callable[[datetime], bool]
