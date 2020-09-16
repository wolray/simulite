from simulite.env import *


def f(name: str) -> Action:
    def _f(t):
        print(f'{name} at {t}')

    return _f


def terminate(t: datetime):
    return t.day > datetime.now().day


def starter(env: Environment):
    t = datetime.now()
    env.push(t, f('a'))
    env.repeat(t, timedelta(hours=1), f('repeat'), terminate)
    env.push(t + timedelta(seconds=10), f('b'))
    env.push(t + timedelta(seconds=10), f('c'))
    env.push(t + timedelta(seconds=20), f('d')).append(f('e'))
    env.push(t + timedelta(seconds=30), f('f')).prepend(f('g'))


def ender(env: Environment):
    print(f'simulation time_span is {env.time_span()}')


if __name__ == '__main__':
    env = Environment()
    env.add_starter(starter)
    env.run()
    ender(env)

    print(f'total duration is {env.duration}')
