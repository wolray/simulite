from simulation import *


def f1(t):
    print(f'using f1 at {t}')


def f2(t):
    print(f'using f2 at {t}')


class ExampleStarter(Starter):
    def __init__(self):
        super().__init__()
        self.period = timedelta(hours=1)
        self.delayed = False

    def before(self):
        t = datetime.now()
        self.push(t, f1)
        self.push(t + timedelta(seconds=10), f1)
        self.push(t + timedelta(seconds=10), f2)
        self.push(t + timedelta(seconds=25), f1).with_after(f2)

    def act(self, t: datetime):
        print(f'repeating at {t}')

    def after(self):
        print(f'simulation time_span is {self.event_bus.time_span()}')

    def allow_repeat(self, t: datetime) -> bool:
        return t.date().day <= datetime.now().day


if __name__ == '__main__':
    sim = Simulation()
    sim.add_starter(ExampleStarter())
    sim.run(datetime.now())
    print(f'total duration is {sim.duration}')
