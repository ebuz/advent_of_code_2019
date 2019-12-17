from itertools import combinations
from operator import add, mul
from math import gcd

def calculate_velocity(p1, p2):
    if p1 == p2:
        return 0
    return 1 if p1 < p2 else -1

def update_velocities(bodies):
    for m,n in combinations(range(len(bodies)), 2):
        adjust_m = list(map(calculate_velocity, bodies[m][0], bodies[n][0]))
        bodies[m][1] = list(map(add, bodies[m][1], adjust_m))
        bodies[n][1] = list(map(add, bodies[n][1], map(mul, adjust_m, [-1] * len(adjust_m))))
    return bodies

def update_positions(bodies):
    for m in range(len(bodies)):
        bodies[m][0] = list(map(add, bodies[m][1], bodies[m][0]))
    return bodies

def setup_simulation(moon_pos):
    moon_pos = moon_pos.strip().split('\n')
    moon_pos = [[int(p.strip('<>xyz= ')) for p in m.split(', ')] for m in moon_pos]
    return [[m, [0] * len(m)] for m in moon_pos]

def setup_sub_simulation(moon_pos, dimension = 0):
    moon_pos = moon_pos.strip().split('\n')
    moon_pos = [[int(p.strip('<>xyz= ')) for p in m.split(', ')] for m in moon_pos]
    return [[m[dimension:dimension+1], [0]] for m in moon_pos]

def simulator(bodies):
    yield bodies
    while True:
        bodies = update_positions(update_velocities(bodies))
        yield bodies

def calculate_total_energy(bodies):
    return sum(mul(*[sum(abs(v) for v in f) for f in m]) for m in bodies)

def simulate_n_steps(moon_pos, steps = 1000):
    simulation = simulator(setup_simulation(moon_pos))
    bodies = next(simulation)
    for i in range(steps):
        bodies = next(simulation)
    return bodies

def lcm(a, b):
    return a * b // gcd(a, b)

def simulate_to_repetition(moon_pos):
    periods = []
    for i in range(3):
        simulation = simulator(setup_sub_simulation(moon_pos, i))
        first_state = str(next(simulation))
        count = 1
        while str(next(simulation)) != first_state:
            count = count + 1
        periods.append(count)
    return lcm(periods[0], lcm(*periods[1:]))

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(f'{calculate_total_energy(simulate_n_steps(problem_input.read()))}')
    with open('part1_input.txt') as problem_input:
        result = simulate_to_repetition(problem_input.read())
        print(f'{result}')
