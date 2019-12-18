import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import defaultdict
import curses

from intcode import evolve_state

tile_id_map = {
        '0': ' ',
        '1': '|',
        '2': '=',
        '3': '-',
        '4': 'o'
        }

def run_game(program):
    state = (program.split(','), 0, 0, [], [])
    try:
        while state[0][state[1]][-2:] != '99':
            if len(state[4]) == 3: # update screen
                yield state[4] # includes x, y, tile_id
                state = (state[0], state[1], state[2], state[3], [])
            else:
                state = evolve_state(state)
        if len(state[4]) > 0:
            yield state[4]
    except GeneratorExit:
        pass

def render_grid(program):
    game = run_game(program)
    grid = defaultdict(lambda: ' ')
    for i in game:
        x, y, tile_id = i
        grid[(int(x),int(y))] = tile_id_map[tile_id]
    painted_points = list(grid.keys())
    right = max(int(i[0]) for i in painted_points)
    bottom = max(int(i[1]) for i in painted_points)
    display = []
    for y in range(bottom + 1):
        display.append([' ' for x in range(right + 1)])
    for p in painted_points:
        x, y = p
        display[y][x] = grid[p]
    display = [''.join(i) for i in display]
    display = '\n'.join(display)
    return display

def sign(x):
    return (x>0) - (x<0)

def display_game(program, saved_moves = [], auto_play = False):
    def curses_display(stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, 'autoplay? y/n')
        stdscr.refresh()
        auto_play = stdscr.getkey() == 'y'
        stdscr.clear()
        stdscr.refresh()
        state = (['2']+program.split(',')[1:], 0, 0, saved_moves, [])
        current_score = 0
        ball_posX = 0
        pad_posX = 0
        while state[0][state[1]][-2:] != '99':
            if len(state[4]) == 3: # update screen
                x, y, tile_id = state[4]
                if int(x) < 0: # score
                    stdscr.addstr(30, 0, tile_id)
                    current_score = tile_id
                else:
                    stdscr.addch(int(y), int(x), tile_id_map[tile_id])
                    if tile_id == '4':
                        ball_posX = int(x)
                    if tile_id == '3':
                        pad_posX = int(x)
                state = (state[0], state[1], state[2], state[3], [])
            if state[0][state[1]][-1] == '3' and len(state[3]) < 1: # need input
                if not auto_play:
                    stdscr.addstr(31, 0, 'move ?')
                    stdscr.refresh()
                    next_move = stdscr.getch()
                    if next_move == 260:
                        stdscr.addstr(31, 0, 'move l')
                        next_move = ['-1']
                    elif next_move == 261:
                        stdscr.addstr(31, 0, 'move r')
                        next_move = ['1']
                    else:
                        stdscr.addstr(31, 0, 'move c')
                        next_move = ['0']
                else:
                    next_move = [str(sign(ball_posX - pad_posX))]
                state = (state[0], state[1], state[2], next_move, state[4])
            stdscr.refresh()
            state = evolve_state(state)
        stdscr.addstr(31, 0, 'game over, again? y/n')
        stdscr.refresh()
        return current_score, stdscr.getkey()
    return curses_display


if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        final_grid = render_grid(problem_input.read())
        print(str(final_grid.count('=')))
    with open('part1_input.txt') as problem_input:
        repeat = True
        program = str(problem_input.read())
        while repeat:
            score, prompt = curses.wrapper(display_game(program))
            repeat = True if prompt == 'y' else False
        print(str(f'last score: {score}'))

