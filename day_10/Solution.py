from math import sqrt, asin, degrees, isclose
from collections import defaultdict
from itertools import cycle

def calculate_angles(i, j):
    if i[0] == j[0]:
        return 90, 270
    if i[1] == j[1]:
        return 0, 180
    x = abs(i[0] - j[0])
    y = abs(i[1] - j[1])
    if x == y: #equilateral, no need for maths
        if i[0] - j[0] < 0:
            return 45, 225
        return 135, 315
    if x < y: # j is smaller angle in triangle
        ang_j = degrees(asin(x/sqrt(x**2 + y**2)))
        ang_i = 90 - ang_j
    else:
        ang_i = degrees(asin(y/sqrt(x**2 + y**2)))
        ang_j = 90 - ang_i
    if i[0] < j[0]:
        return ang_i, 270 - ang_j
    return 180 - ang_i, 270 + ang_j


def analyze_map(asteroid_map):
    width = asteroid_map.index('\n')
    height = asteroid_map.strip().count('\n') + 1
    asteroid_coords = []
    for y,line in enumerate(asteroid_map.strip().split('\n')):
        for x,c in enumerate(line.rstrip('.')):
            if c == '#':
                asteroid_coords.append((x,y))
    return width, height, asteroid_coords

def pretty_print(asteroids_visible, width, height):
    print_map = [['.'] * width] * height # [y][x]
    for a in asteroids_visible.keys():
        print_map[a[1]][a[0]] = str(len(asteroids_visible[a].keys()))
    print('\n'.join([''.join(i) for i in print_map]))

def tabulate_over_asteroids(asteroid_map):
    width, height, asteroid_coords = analyze_map(asteroid_map)
    asteroids_visible = defaultdict(lambda: defaultdict(list)) #asteroid_coords -> angle -> list
    for i,i_coords in enumerate(asteroid_coords):
        for j,j_coords in enumerate(asteroid_coords[i+1:]):
            angle_i, angle_j = calculate_angles(i_coords, j_coords)
            angle_i = round(angle_i, 10)
            angle_j = round(angle_j, 10)
            asteroids_visible[i_coords][angle_i].append(j_coords)
            asteroids_visible[j_coords][angle_j].append(i_coords)
    best = max(asteroids_visible, key = lambda c: len(asteroids_visible[c].keys()))
    return best, len(asteroids_visible[best].keys()), asteroids_visible[best]

def distance(i, j):
    return sqrt(abs(i[0] - j[0])**2 + abs(i[1] - j[1])**2)

def count_down_vaporized(best, best_map):
    for angle in best_map.keys():
        best_map[angle] = sorted(best_map[angle], key = lambda c: distance(c, best))
    angles = sorted(best_map.keys())
    rotation = cycle(angles)
    next_direction = next(rotation)
    if any(i >= 270 for i in angles):
        while next_direction < 270:
            next_direction = next(rotation)
    for i in range(200):
        last_vaporized = best_map[next_direction].pop(0)
        next_direction = next(rotation)
    return last_vaporized

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        best, visible, best_map = tabulate_over_asteroids(problem_input.read())
        print(f'{best}, {visible}')
        last_vaporized = count_down_vaporized(best, best_map)
        print(str(last_vaporized[0] * 100 + last_vaporized[1]))
