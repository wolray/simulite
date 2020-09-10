import abc

from event import *


class AbsRouter(Action):
    def __init__(self):
        self.priority: int = 0
        self.event_bus: Optional[EventBus] = None

    @abc.abstractmethod
    def __call__(self, t: datetime):
        pass

    def push(self, t: datetime, action: Action) -> Event:
        return self.push_event(self.event(t, action))

    def push_event(self, event: Event) -> Event:
        self.event_bus.push(event)
        return event

    def event(self, t: datetime, action: Action) -> Event:
        return Event(t, self.priority, action)


class Starter(AbsRouter):
    def __init__(self):
        super(Starter, self).__init__()
        self.start_time: [datetime] = None
        self.period: Optional[timedelta] = None
        self.delayed = False

    def before(self):
        pass

    def act(self, t: datetime):
        pass

    def after(self):
        pass

    def __call__(self, t: datetime):
        if self.period is None:
            self.act(t)
        else:
            if not self.delayed:
                self.act(t)
            self._push_repeat(t)

    def allow_repeat(self, t: datetime) -> bool:
        """
        condition for repeat
        :param t: current time
        :return: if allowing repeat
        """
        pass

    def _push_repeat(self, t):
        self.push(t + self.period, self._repeat)

    def _repeat(self, t):
        if self.allow_repeat(t):
            self.act(t)
            self._push_repeat(t)
