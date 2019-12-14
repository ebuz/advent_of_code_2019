from itertools import cycle, permutations

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

def run_phase_program(program, initial_input = ['5']):
    phase = initial_input[0]
    state = (program.split(','), 0, initial_input, [])
    try:
        while state[0][state[1]][-2:] != '99':
            if state[0][state[1]][-1] == '4': # about to hit next output
                state = evolve_state(state)
                yield state[3]
                next_input = (yield)
                assert next_input is not None
                state = (state[0], state[1], next_input, [])
            else:
                state = evolve_state(state)
        if len(state[3]) > 0:
            yield state[3]
    except GeneratorExit:
        pass

def loop_programs(program, phases = ['9', '8', '7', '6', '5']):
    amps = []
    lastOutput = None
    for i,p in enumerate(phases):
        if i == 0:
            amps.append(run_phase_program(program, [p, '0']))
        else:
            amps.append(run_phase_program(program, [p] + lastOutput))
        lastOutput = next(amps[i])
    for i in cycle([0, 1, 2, 3, 4]):
        try:
            next(amps[i])
            lastOutput = amps[i].send(lastOutput)
        except Exception as e:
            break
    return lastOutput[0]

def run_to_output(state):
    if type(state) == str:
        state = (state.split(','), 0, [], [])
    elif type(state[0]) == str:
        state = (state[0].split(','), state[1], state[2], state[3])
    while len(state[3]) < 1:
        state = evolve_state(state)
    return state

def run_to_halt(state):
    if type(state) == str:
        state = (state.split(','), 0, [], [])
    elif type(state[0]) == str:
        state = (state[0].split(','), state[1], state[2], state[3])
    while state[0][state[1]][-2:] != '99':
        state = evolve_state(state)
    return state

def search_phase_sequences(program, phases = ['0', '1', '2', '3', '4']):
    thruster_outputs = []
    phases = set(phases)
    for a in phases:
        subphase_a = phases.copy() - set([a]) # 4 items
        output_a = run_to_output((program, 0, [a, '0'], []))[3][-1]
        for b in subphase_a:
            subphase_b = subphase_a.copy() - set([b]) # 3 items
            output_b = run_to_output((program, 0, [b, output_a], []))[3][-1]
            for c in subphase_b:
                subphase_c = subphase_b.copy() - set([c]) # 2 items
                output_c = run_to_output((program, 0, [c, output_b], []))[3][-1]
                for d in subphase_c:
                    subphase_d = subphase_c.copy() - set([d]) #1 item
                    output_d = run_to_output((program, 0, [d, output_c], []))[3][-1]
                    for e in subphase_d:
                        output_e = run_to_output((program, 0, [e, output_d], []))[3][-1]
                        thruster_outputs.append(int(output_e))
    return str(max(thruster_outputs))

def search_repeating_phase_sequences(program, phases = ['5', '6', '7', '8', '9']):
    outputs = []
    for p in permutations(phases):
        outputs.append(int(loop_programs(program, p)))
    return str(max(outputs))

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(search_phase_sequences(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(search_repeating_phase_sequences(problem_input.read())))

