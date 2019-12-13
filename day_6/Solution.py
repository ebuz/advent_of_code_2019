from collections import defaultdict

def tree():
    return defaultdict(tree)

def walk_orbits(mass, orbit_map, orbit_memo):
    for s in orbit_map[mass]:
        orbit_memo[s] = 1 + orbit_memo[mass]
        orbit_memo = walk_orbits(s, orbit_map, orbit_memo)
    return orbit_memo

def tabulate_orbits(orbit_map_string):
    orbit_map = defaultdict(list)
    for line in orbit_map_string.split():
        m, s = line.strip().split(')')
        orbit_map[m].append(s)
    orbit_memo = {'COM': 0}
    orbit_memo = walk_orbits('COM', orbit_map, orbit_memo)
    return sum(orbit_memo.values())

def orbit_transfers(orbit_map_string):
    orbit_map = dict()
    for line in orbit_map_string.split():
        m, s = line.strip().split(')')
        orbit_map[s] = m
    my_path_to_com = [orbit_map['YOU'],]
    while my_path_to_com[-1] != 'COM':
        my_path_to_com.append(orbit_map[my_path_to_com[-1]])
    santa_path_to_com = [orbit_map['SAN'],]
    while santa_path_to_com[-1] != 'COM' and santa_path_to_com[-1] not in my_path_to_com:
        santa_path_to_com.append(orbit_map[santa_path_to_com[-1]])
    intersection = my_path_to_com.index(santa_path_to_com[-1])
    return len(santa_path_to_com) + len(my_path_to_com[:intersection]) - 1

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(tabulate_orbits(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(orbit_transfers(problem_input.read())))
