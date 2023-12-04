#! /usr/bin/env python3

import sys, os
import pprint


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Find the sum of the part numbers in the engine schematic.")
    print("Part 2: Add up all the gear ratios in the engine schematic.\n")
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


def adjacentNumberSearch(x, y, grid):
    nums = []
    width = len(grid[0])
    height = len(grid)
    def findNum(x, y):
        startX = x
        endX = x
        while startX >= 0 and grid[y][startX].isnumeric():
            startX -= 1
        while endX < width and grid[y][endX].isnumeric():
            endX += 1
        num = int( "".join(grid[y][startX + 1: endX]))
        span = (startX + 1, endX, y)
        return num, span
    
    def verifyChecked(x, y, chk):
        for start, end, cY in chk:
            if y == cY and x >= start and x < end:
                return True
        return False

    coords = []
    coords += [(i,j) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)]
    checked = []
    for cX, cY in coords:
        # Skip over coordinates that were checked
        if verifyChecked(cX, cY, checked):
            continue
        if grid[cY][cX].isnumeric():
            if cX < 0 or cX >= width or cY < 0 or cY >= height:
                continue
            num, span = findNum(cX, cY)
            checked.append(span)
            nums.append(num)

    return list(nums)

def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    grid = []
    for line in lines:
        grid.append([x for x in line.strip()])
    width = len(grid[0])
    height = len(grid)

    if part == 1:
        # Find all part numbers
        part_numbers = []
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
    else:
        # Find all gear ratios
        gear_ratios = []
        for y in range(height):
            for x in range(width):
                if grid[y][x] == "*":
                    nums = adjacentNumberSearch(x, y, grid)
                    print(nums)
                    ratio = 1 if len(nums) == 2 else 0
                    for num in nums:
                        ratio *= num
                    gear_ratios.append(ratio)

    
    if part == 1:
        print(f"The sum of each calibration value is {sum(part_numbers)}")
    else:
        print(f"The sum of the gear ratios is {sum(gear_ratios)}")


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