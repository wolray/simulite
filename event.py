from datetime import datetime, timedelta
from queue import PriorityQueue
from typing import Callable, Optional, Dict

Action = Callable[[datetime], None]


class Event:
    def __init__(self, time: datetime, priority: int, action: Action):
        self.time = time
        self.key = (time, priority)
        self.action = action

    @staticmethod
    def merge(a: Action, b: Action):
        def new(t):
            a(t)
            b(t)

        return new

    def prepend(self, action: Action):
        self.action = Event.merge(action, self.action)

    def append(self, action: Action):
        self.action = Event.merge(self.action, action)


class EventBus:
    def __init__(self):
        self.pq = PriorityQueue()
        self.map: Dict[tuple, Event] = {}
        self.beg: Optional[datetime] = None
        self.now: Optional[datetime] = None
        self.end: Optional[datetime] = None

    def push(self, event: Event):
        """
        push an event onto the queue
        merge if the key is duplicated
        :param event: event to push
        :return: pushed event if not merged else the old one
        """
        key = event.key
        old = self.map.get(key)
        if old:
            old.append(event.action)
            return old
        else:
            self.pq.put(key)
            self.map[key] = event
            return event

    def pop(self) -> Event:
        key = self.pq.get()
        return self.map.pop(key)

    def run(self):
        while not self.pq.empty():
            event = self.pop()
            t = event.time
            if self.beg is None:
                self.beg = t
            self.now = t
            event.action(t)
            yield
        self.close()

    def close(self):
        self.end = self.now

    def time_span(self) -> Optional[timedelta]:
        """
        :return: time span between the first and the last events
        """
        return self.end - self.beg if self.end else None
