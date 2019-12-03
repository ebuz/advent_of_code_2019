# Intcode
# program lines: (1|2|99, w, x, y, ..., z)
# position 0 is opcode
# opcode 1: add inputs at positions w and x and write result to position y
# opcode 2: multiplies inputs at positions w and x and write result to position y
# opcode 99: stop
# after operation move forward 4 spots and repeat

def evolve_state(program, position = 0):
    if type(program) == str:
        program = [int(c) for c in program.split(',')]
    if type(program[position]) == str:
        program = [int(c) for c in program]
    if program[position] == 99:
        return program
    if program[position] == 1:
        program[program[position + 3]] = program[program[position + 1]] + program[program[position + 2]]
        return program
    if program[position] == 2:
        program[program[position + 3]] = program[program[position + 1]] * program[program[position + 2]]
        return program
    raise Exception

def run_program(program):
    position = 0
    if type(program) == str:
        program = [int(c) for c in program.split(',')]
    while program[position] != 99:
        program = evolve_state(program, position)
        position = position + 4
    return program

def restore_and_run_program(program, noun = 12, verb = 2):
    if type(program) == str:
        program = [int(c) for c in program.split(',')]
    program[1] = noun
    program[2] = verb
    program = run_program(program)
    return program[0]

def back_solve_input(program, output = 19690720):
    for i in range(100):
        for j in range(100):
            result = restore_and_run_program(program, i, j)
            if result == output:
                return (100 * i) + j
    return None


if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(restore_and_run_program(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(back_solve_input(problem_input.read())))
