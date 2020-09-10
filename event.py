from datetime import datetime, timedelta
from queue import PriorityQueue
from typing import Callable, Optional

Action = Callable[[datetime], None]


class Event:
    def __init__(self, time: datetime, priority: int, action: Action):
        self.time = time
        self.priority = priority
        self.action = action

    def trigger(self):
        """
        trigger the event by running the action
        """
        self.action(self.time)

    def with_before(self, action: Action):
        old = self.action

        def new(t):
            action(t)
            old(t)

        self.action = new

    def with_after(self, action: Action):
        old = self.action

        def new(t):
            old(t)
            action(t)

        self.action = new

    def __lt__(self, other):
        if self.time < other.time:
            return True
        return self.time == other.time and self.priority < other.priority

    def __le__(self, other):
        if self.time < other.time:
            return True
        return self.time == other.time and self.priority <= other.priority

    def __eq__(self, other):
        return self.time == other.time and self.priority == other.priority

    def __gt__(self, other):
        if self.time > other.time:
            return True
        return self.time == other.time and self.priority > other.priority

    def __ge__(self, other):
        if self.time > other.time:
            return True
        return self.time == other.time and self.priority >= other.priority


class EventBus:
    def __init__(self):
        self.pq = PriorityQueue()
        self.beg: Optional[datetime] = None
        self.now: Optional[datetime] = None
        self.end: Optional[datetime] = None

    def push(self, event: Event):
        """
        push an event onto the queue
        :param event: event to push
        """
        self.pq.put(event)

    def run(self):
        while not self.pq.empty():
            event = self.pq.get()
            if self.beg is None:
                self.beg = event.time
            self.now = event.time
            event.trigger()
            yield
        self.close()

    def close(self):
        self.end = self.now

    def time_span(self) -> Optional[timedelta]:
        """
        :return: time span between the first and the last events
        """
        return self.end - self.beg if self.end else None
