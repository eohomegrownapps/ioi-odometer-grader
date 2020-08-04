import simulator as odo

import argparse
import math


def get_grid(fin):
    grid = [[0] * odo.DEFAULT_GRID_SIDE for i in range(odo.DEFAULT_GRID_SIDE)]
    odo.load_grid(fin, grid)
    return grid


def run_sim(grid, program, max_steps, max_program_size, use_compile=False):
    grid = grid.splitlines()
    s = odo.Simulation(odo.DEFAULT_GRID_SIDE, debug=False, max_steps=max_steps)
    odo.load_grid(grid, s.grid)
    try:
        s.load_program(program.splitlines())
    except odo.ParserException as e:
        return (False, "Could not parse source code:\n%s" % (e))
    s.execute_program(compilation=use_compile)

    if s.instruction_num > max_program_size:
        return (False, "Maximum program size exceeded")
    if s.killed:
        if s.step_num >= max_program_size:
            return (False, "Program killed")
        else:
            return (False, "Maximum execution length exceeded")
    return (True, s)


def checkSubtask1(grid, program, use_compile=False):
    max_program_size = 100
    max_execution_length = 1000
    initial_grid = get_grid(grid.splitlines())
    result = run_sim(
        grid, program, max_execution_length, max_program_size, use_compile=use_compile
    )
    if result[0] is False:
        return result
    s = result[1]

    x = initial_grid[0][0]
    y = initial_grid[1][0]
    success = False

    if x <= y and s.posx == 0 and s.posy == 0:
        success = True
    elif x > y and s.posx == 1 and s.posy == 0:
        success = True

    if success:
        return (True, 1)
    else:
        return (False, "Wrong Answer")


def checkSubtask2(grid, program, use_compile=False):
    max_program_size = 200
    max_execution_length = 2000
    initial_grid = get_grid(grid.splitlines())
    result = run_sim(
        grid, program, max_execution_length, max_program_size, use_compile=use_compile
    )
    if result[0] is False:
        return result
    s = result[1]

    x = initial_grid[0][0]
    y = initial_grid[1][0]
    success = False

    if x == s.grid[0][0] and y == s.grid[1][0]:
        if x <= y and s.posx == 0 and s.posy == 0:
            success = True
        elif x > y and s.posx == 1 and s.posy == 0:
            success = True

    if success:
        return (True, 1)
    else:
        return (False, "Wrong Answer")


def checkSubtask3(grid, program, use_compile=False):
    max_program_size = 100
    max_execution_length = 200000
    initial_grid = get_grid(grid.splitlines())
    result = run_sim(
        grid, program, max_execution_length, max_program_size, use_compile=use_compile
    )
    if result[0] is False:
        return result
    s = result[1]

    pebbles = []
    for x in range(odo.DEFAULT_GRID_SIDE):
        if initial_grid[x][0] > 0:
            pebbles.append(x)

    success = False
    if s.posx == (pebbles[0] + pebbles[1]) // 2 and s.posy == 0:
        success = True

    if success:
        return (True, 1)
    else:
        return (False, "Wrong Answer")


def checkSubtask4(grid, program, use_compile=False):
    max_program_size = 200
    max_execution_length = 2000000
    initial_grid = get_grid(grid.splitlines())
    result = run_sim(
        grid, program, max_execution_length, max_program_size, use_compile=use_compile
    )
    if result[0] is False:
        return result
    s = result[1]

    pebblecnt = sum([sum(row) for row in initial_grid])

    success = False
    if s.grid[0][0] == pebblecnt and sum([sum(row) for row in s.grid]) == pebblecnt:
        success = True

    if success:
        length = s.step_num
        if length <= 200000:
            return (True, 1)
        else:
            return (True, 1 - math.log10(length / 200000))
    else:
        return (False, "Wrong Answer")


def checkSubtask5(grid, program, use_compile=False):
    max_program_size = 4440
    max_execution_length = 44400000
    initial_grid = get_grid(grid.splitlines())
    result = run_sim(
        grid, program, max_execution_length, max_program_size, use_compile=use_compile
    )
    if result[0] is False:
        return result
    s = result[1]

    success = True
    if initial_grid != s.grid:
        success = False
    else:
        minpebbles = initial_grid[s.posx][s.posy]
        if min([min(row) for row in initial_grid]) != minpebbles:
            success = False

    if success:
        length = s.instruction_num
        if length <= 444:
            return (True, 1)
        else:
            return (True, 1 - math.log10(length / 444))
    else:
        return (False, "Wrong Answer")


def main():
    parser = argparse.ArgumentParser(description="Odometer grader")
    parser.add_argument('-g', '--grid', dest='grid_file',
                        action='store', default=None,
                        type=str,
                        help="grid description file (default: empty grid)")
    parser.add_argument('program',
                        action='store', type=str,
                        help="program to run")
    parser.add_argument('-c', '--compile', dest='compile',
                        action='store_true', default=False,
                        help="compile the program instead of interpreting it")
    parser.add_argument('-s', '--subtask', dest='subtask',
                        action='store', default=None,
                        metavar='SUBTASK', type=int,
                        help="Subtask number to evaluate")

    args = parser.parse_args()
    subtask = args.subtask

    with open(args.program) as fin:
        program = fin.read()

    with open(args.grid_file) as fin:
        grid = fin.read()

    result = None

    if subtask == 1:
        result = checkSubtask1(grid, program)
    elif subtask == 2:
        result = checkSubtask2(grid, program)
    elif subtask == 3:
        result = checkSubtask3(grid, program)
    elif subtask == 4:
        result = checkSubtask4(grid, program)
    elif subtask == 5:
        result = checkSubtask5(grid, program)
    else:
        print("Invalid subtask")
    print(result)


if __name__ == '__main__':
    main()
