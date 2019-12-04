def is_valid_adjusted(password, length = 6):
    pl = sorted(list(password))
    if ''.join(pl) != password:
        return False
    unique = set(pl)
    if len(unique) >= length or len(password) > length:
        return False
    return any(pl.count(d) == 2 for d in unique)

def is_valid(password, length = 6):
    pl = sorted(list(password))
    if ''.join(pl) != password:
        return False
    return len(password) == length and len(set(pl)) < length

def count_passwords_brute(start, end, length = 6, evaluator = is_valid):
    counts = 0
    for p in range(int(start), int(end) + 1):
        if evaluator(str(p).zfill(length), length):
            counts = counts + 1
    return counts

def count_passwords_range(number_range):
    start, end = number_range.split('-')
    return count_passwords_brute(start, end, len(start))

def count_passwords_range_adjusted(number_range):
    start, end = number_range.split('-')
    return count_passwords_brute(start, end, len(start), is_valid_adjusted)

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(count_passwords_range(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(count_passwords_range_adjusted(problem_input.read())))
