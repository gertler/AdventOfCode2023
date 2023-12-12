#! /usr/bin/env python3

import sys, os
import math


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Find how many steps along the loop it takes to be the farthest from the starting position.")
    print("Part 2: \n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def nextPipe(grid, curr, prev):
    conns = []
    tile = grid[curr[1]][curr[0]]
    x = curr[0]
    y = curr[1]

    # Find connecting spaces
    if tile == "|":
        conns = [(x, y + dy) for dy in [-1,1]]
    elif tile == "-":
        conns = [(x + dx, y) for dx in [-1,1]]
    elif tile == "L":
        conns = [(x, y - 1), (x + 1, y)]
    elif tile == "J":
        conns = [(x, y - 1), (x - 1, y)]
    elif tile == "7":
        conns = [(x - 1, y), (x, y + 1)]
    elif tile == "F":
        conns = [(x + 1, y), (x, y + 1)]
    
    new = (set(conns) - set([prev])).pop()
    return new


def startPipe(grid, start):
    x = start[0]
    y = start[1]
    if x - 1 >= 0 and grid[y][x-1] in ["-", "L", "J", "7", "F"]:
        return (x-1, y)
    elif x + 1 < len(grid[y]) and grid[y][x+1] in ["-", "L", "J", "7", "F"]:
        return (x+1, y)
    elif y - 1 >= 0 and grid[y-1][x] in ["|", "L", "J", "7", "F"]:
        return (x, y-1)
    else:
        return (x, y+1)



def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    # Set the grid and start index
    grid = []
    start = None
    for i in range(len(lines)):
        g = [x for x in lines[i].strip()]
        if "S" in g:
            start = (g.index("S"), i)
        grid.append(g)

    # Make sure we found a start index
    if not start:
        print("Input must have a start index")
        exit(1)
    
    first_pipe = startPipe(grid, start)

    pipe_length = 1
    curr = nextPipe(grid, first_pipe, start)
    prev = first_pipe
    while curr != start:
        pipe_length += 1
        temp = curr
        curr = nextPipe(grid, curr, prev)
        prev = temp


    if part == 1:
        print(f"The number of steps in the loop to be farthest from the starting position is {math.ceil(pipe_length / 2)}")
    else:
        print(f"")


if __name__ == "__main__":
    # Check args:
    if "-h" in sys.argv:
        usage()
        exit(0)
    if len(sys.argv) != 4 or sys.argv[1] != "-p":
        usage()
        exit(1)
    
    # Verify part
    if not sys.argv[2].isnumeric():
        usage()
        exit(1)
    part = int(sys.argv[2])
    if part not in [1,2]:
        usage()
        exit(1)
    
    # Verify input file exists
    if not os.path.isfile(sys.argv[3]):
        usage()
        exit(1)
    
    # Go
    main(sys.argv[3], part)