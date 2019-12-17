from collections import defaultdict

def parse_parameter_modes(opcode):
    if len(opcode) == 1:
        opcode = '0' + opcode
    parameter_modes = opcode[:-2]
    opcode = opcode[-2:]
    if opcode == '99':
        return []
    if opcode in ['01', '02', '07', '08']:
        parameter_modes = ['0'] * (3 - len(parameter_modes)) + list(parameter_modes)
    elif opcode in ['05', '06']:
        parameter_modes = ['0'] * (2 - len(parameter_modes)) + list(parameter_modes)
    elif opcode in ['03', '04', '09']:
        parameter_modes = ['0'] * (1 - len(parameter_modes)) + list(parameter_modes)
    else:
        raise Exception
    return list(reversed(parameter_modes))

def extend_to_index(index, program):
    if index >= len(program):
        program = program + ['0'] * (index - (len(program) - 1))
    return program

def safe_get(index, program):
    program = extend_to_index(index, program)
    return program[index], program

def safe_put(index, value, program):
    program = extend_to_index(index, program)
    program[index] = value
    return program

def modal_get(parameter, mode, program, r_base):
    if mode == '0':
        return safe_get(int(parameter), program)
    if mode == '2':
        return safe_get(int(parameter) + r_base, program)
    return parameter, program

def modal_put(value, parameter, mode, program, r_base):
    if mode == '0':
        return safe_put(int(parameter), value, program)
    if mode == '2':
        return safe_put(int(parameter) + r_base, value, program)
    raise Exception

def evolve_state(state = ('99,0', 0, 0, [], [])):
    program, position, r_base, inputs, outputs = state
    if type(program) == str:
        program = program.split(',')
    if program[position][-2:] == '99':
        return state
    parameter_modes = parse_parameter_modes(program[position])
    if program[position][-1] in ['1', '2', '4', '5', '6', '7', '8', '9']:
        a, program = modal_get(program[position + 1], parameter_modes[0], program, r_base)
        a = int(a)
        if program[position][-1] not in ['4', '9']:
            b, program = modal_get(program[position + 2], parameter_modes[1], program, r_base)
            b = int(b)
    if program[position][-1] in ['1', '2', '7', '8']:
        if program[position][-1] == '1':
            new_value = str(a + b)
        elif program[position][-1] == '2':
            new_value = str(a * b)
        elif program[position][-1] == '8':
            new_value = '1' if a == b else '0'
        else:
            new_value = '1' if a < b else '0'
        program = modal_put(new_value, program[position + 3], parameter_modes[2], program, r_base)
        position = position + 4
    elif program[position][-1] in ['5', '6']:
        if program[position][-1] == '5' and a != 0:
            position = b
        elif program[position][-1] == '6' and a == 0:
            position = b
        else:
            position = position + 3
    elif program[position][-1] in ['3', '4']:
        if program[position][-1] == '3':
            program = modal_put(inputs.pop(0), program[position + 1], parameter_modes[0], program, r_base)
        else:
            outputs.append(str(a))
        position = position + 2
    elif program[position][-1] == '9':
        r_base = r_base + a
        position = position + 2
    else:
        raise Exception
    return (program, position, r_base, inputs, outputs)

def run_paint_program(program):
    next_input = (yield)
    state = (program.split(','), 0, 0, [next_input], [])
    try:
        while state[0][state[1]][-2:] != '99':
            if len(state[4]) == 2: # paint and move ready
                yield state[4] # includes paint color and direction
                next_input = (yield) # need next input
                assert next_input is not None
                state = (state[0], state[1], state[2], [next_input], [])
            else:
                state = evolve_state(state)
        if len(state[4]) > 0:
            yield state[4]
    except GeneratorExit:
        pass

def run_paint_bot(program, starting_color = '0'):
    grid = defaultdict(lambda: '0')
    x, y = 0, 0
    grid[(x,y)] = starting_color
    directions = ['u', 'r', 'd', 'l']
    paint_program = run_paint_program(program)
    while True:
        try:
            next(paint_program)
            paint, move = paint_program.send(grid[(x, y)])
        except Exception as e:
            print(str(e))
            break
        grid[(x, y)] = paint
        if move == '0':
            directions.insert(0, directions.pop())
        else:
            directions.append(directions.pop(0))
        if directions[0] == 'u':
            y = y + 1
        elif directions[0] == 'r':
            x = x + 1
        elif directions[0] == 'd':
            y = y - 1
        else:
            x = x - 1
    return grid

def render_grid(program):
    grid = run_paint_bot(program, '1')
    painted_points = grid.keys()
    left = min([i[0] for i in painted_points])
    right = max([i[0] for i in painted_points])
    top = max([i[1] for i in painted_points])
    bottom = min([i[1] for i in painted_points])
    display = []
    for y in range((top - bottom + 1)):
        display.append(['◾️' for x in range(right - left + 1)])
    for p in painted_points:
        x, y = p
        display[abs(top - y)][abs(left - x)] = '◾️' if grid[p] == '0' else '◽️'
    display = [''.join(i) for i in display]
    display = '\n'.join(display)
    return display

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(len(run_paint_bot(problem_input.read()))))
    with open('part1_input.txt') as problem_input:
        print(str(render_grid(problem_input.read())))

