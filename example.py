from simulation import *


def f(name: str):
    def ff(t):
        print(f'{name} at {t}')

    return ff


class ExampleStarter(Starter):
    def __init__(self):
        super().__init__()
        self.period = timedelta(hours=1)
        self.delayed = False

    def before(self):
        t = datetime.now()
        self.push(t, f('a'))
        self.push(t + timedelta(seconds=10), f('b'))
        self.push(t + timedelta(seconds=10), f('c'))
        self.push(t + timedelta(seconds=20), f('d')).append(f('e'))
        self.push(t + timedelta(seconds=30), f('f')).prepend(f('g'))

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
