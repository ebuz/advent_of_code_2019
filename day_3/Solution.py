def manhattan_distance(point):
    return sum([abs(i) for i in point])

def steps_to_point(path, point):
    for i,p in enumerate(path):
        if p == point:
            return i
    return None

def convert_move_to_path(moves):
    if type(moves) == str:
        moves = [m for m in moves.split(',')]
    path = [(0,0),]
    for move in moves:
        for steps in range(int(move[1:])):
            x, y = path[-1]
            if move[0] == 'U':
                path.append((x, y + 1))
            elif move[0] == 'R':
                path.append((x + 1, y))
            elif move[0] == 'D':
                path.append((x, y - 1))
            else:
                path.append((x - 1, y))
    return path

def nearest_cross(moves):
    pathA, pathB = [set(convert_move_to_path(m)) for m in moves.split()]
    intersects = pathA.intersection(pathB)
    intersects = list(intersects)
    intersects.sort(key=manhattan_distance)
    return manhattan_distance(intersects[1])

def nearest_cross_path(moves):
    pathA, pathB = [convert_move_to_path(m) for m in moves.split()]
    intersects = set(pathA).intersection(set(pathB))
    combined_distance = []
    for i in list(intersects):
        combined_distance.append(steps_to_point(pathA, i) + steps_to_point(pathB, i))
    combined_distance.sort()
    return combined_distance[1]

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(nearest_cross(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(nearest_cross_path(problem_input.read())))
