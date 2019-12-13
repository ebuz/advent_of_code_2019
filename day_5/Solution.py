# Intcode
# program lines: (1|2|99, w, x, y, ..., z)
# position 0 is opcode
# opcode 1: add inputs at positions w and x and write result to position y
# opcode 2: multiplies inputs at positions w and x and write result to position y
# opcode 3: saves an input to the position given by parameter
# opcode 4: returns value at position given by parameter
# opcode 5: jump-if-true if parameter w is not zero, set next instruction as parameter y, else next instruction is after y
# opcode 6: jump-if-false if parameter w is zero, set next instruction as parameter y, else next instruction is after y
# opcode 7: less, if parameter w is less than y it stores 1 at third parameter else 0
# opcode 8: equals, if parameters w and y are equal it stores 1 at third parameter else 0
# opcode 99: stop
# after operation move forward 4 spots and repeat

# program state: (program code, position, input, output)
# evolution: state -> state
# stop: state.program_code[position][-2:] == '99'

def parse_parameter_modes(opcode):
    if len(opcode) == 1:
        opcode = '0' + opcode
    parameter_modes = opcode[:-2]
    opcode = opcode[-2:]
    if opcode == '99':
        return []
    if opcode in ['01', '02', '07', '08']:
        parameter_modes = ['0'] * (3 - len(parameter_modes)) + list(parameter_modes)
        parameter_modes[0] = '1'
    elif opcode in ['05', '06']:
        parameter_modes = ['0'] * (2 - len(parameter_modes)) + list(parameter_modes)
    elif opcode == '04':
        parameter_modes = ['0'] * (1 - len(parameter_modes)) + list(parameter_modes)
    else:
        parameter_modes = ['1']
    return list(reversed(parameter_modes))

def interpret_parameter(parameter, mode, program):
    if mode == '0':
        return program[int(parameter)]
    return parameter

def evolve_state(state = ('99,0', 0, [], [])):
    program, position, inputs, outputs = state
    if type(program) == str:
        program = program.split(',')
    parameter_modes = parse_parameter_modes(program[position])
    if program[position][-1] in ['1', '2']:
        a, b, c = [int(interpret_parameter(p, m, program)) for p,m in zip(program[position + 1:position + 4], parameter_modes)]
        if program[position][-1] == '1':
            program[c] = str(a + b)
        else:
            program[c] = str(a * b)
        position = position + 4
    elif program[position][-1] in ['7', '8']:
        a, b, c = [int(interpret_parameter(p, m, program)) for p,m in zip(program[position + 1:position + 4], parameter_modes)]
        if program[position][-1] == '8':
            program[c] = '1' if a == b else '0'
        else:
            program[c] = '1' if a < b else '0'
        position = position + 4
    elif program[position][-1] in ['5', '6']:
        a, b = [int(interpret_parameter(p, m, program)) for p,m in zip(program[position + 1:position + 3], parameter_modes)]
        if program[position][-1] == '5' and a != 0:
            position = b
        elif program[position][-1] == '6' and a == 0:
            position = b
        else:
            position = position + 3
    elif program[position][-1] in ['3', '4']:
        a = int(interpret_parameter(program[position + 1], parameter_modes[0], program))
        if program[position][-1] == '3':
            program[a] = inputs.pop(0)
        else:
            outputs.append(str(a))
        position = position + 2
    elif program[position][-2:] != '99':
        raise Exception
    return (program, position, inputs, outputs)

def run_to_halt(state):
    if type(state) == str:
        state = (state.split(','), 0, [], [])
    elif type(state[0]) == str:
        state = (state[0].split(','), state[1], state[2], state[3])
    while state[0][state[1]][-2:] != '99':
        state = evolve_state(state)
    return state

def run_diagnostic(program, inputs = ['1']):
    if type(program) == str:
        program = program.strip()
        program = program.split(',')
    state = (program, 0, inputs, [])
    while state[0][state[1]][-2:] != '99':
        state = evolve_state(state)
    return state[3]


if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(run_diagnostic(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(run_diagnostic(problem_input.read(), inputs = ['5'])))
