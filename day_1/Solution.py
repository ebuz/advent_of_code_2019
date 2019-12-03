def calculate_module_fuel(mass):
    return (mass // 3) - 2

def calculate_module_fuel_with_fuel_adjust(mass):
    added_fuel = []
    toAdd = calculate_module_fuel(mass)
    while toAdd > 0:
        added_fuel.append(toAdd)
        toAdd = calculate_module_fuel(added_fuel[-1])
    return sum(added_fuel)

def calculate_total_module_fuel(masses):
    fuel_per_mass = [calculate_module_fuel(int(m)) for m in masses.split()]
    return sum(fuel_per_mass)

def calculate_total_module_fuel_adjusted(masses):
    fuel_per_mass = [calculate_module_fuel_with_fuel_adjust(int(m)) for m in masses.split()]
    return sum(fuel_per_mass)

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(calculate_total_module_fuel(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(calculate_total_module_fuel_adjusted(problem_input.read())))
