#! /usr/bin/env python3

import sys, os
import pprint


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Find the sum of the part numbers in the engine schematic.\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def findNextNum(startIndex, row):
    digits = []
    num_index = -1
    for i in range(startIndex, len(row)):
        # If looking at number, parse number
        if row[i].isnumeric():
            num_index = i if num_index == -1 else num_index
            digits.append(row[i])
        # Otherwise, either keep searching or stop once end of number is reached
        elif num_index == -1:
            continue
        else:
            break
    if num_index == -1:
        return (-1, 0)
    num = int( "".join(digits) )
    return (num_index, num)


def adjacentSymbolSearch(startIndex, endIndex, rowIndex, grid):
    width = len(grid[0])
    height = len(grid)
    def hasSymbol(x, y):
        if x < 0 or x >= width or y < 0 or y >= height:
            return False
        return grid[y][x] not in "0123456789."
    
    coords = []
    coords += [(x, rowIndex - 1) for x in range(startIndex - 1, endIndex + 1)]
    coords += [(x, rowIndex + 1) for x in range(startIndex - 1, endIndex + 1)]
    coords += [(startIndex - 1, rowIndex), (endIndex, rowIndex)]
    for cX, cY in coords:
        if hasSymbol(cX, cY):
            return True
    return False


def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    # Find all part numbers
    part_numbers = []
    grid = []
    for line in lines:
        grid.append([x for x in line.strip()])
    width = len(grid[0])
    height = len(grid)

    for y in range(height):
        row = grid[y]
        x = 0
        while x < width:
            # Get start and end indices of next number in row
            start_index, num = findNextNum(x, row)
            if start_index == -1:
                break
            end_index = start_index + len(str(num))
            x = end_index + 1

            # Check if there is a symbol adjacent
            is_part_number = adjacentSymbolSearch(start_index, end_index, y, grid)
            if is_part_number:
                part_numbers.append(num)
    
    if part == 1:
        print(f"The sum of each calibration value is {sum(part_numbers)}")


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