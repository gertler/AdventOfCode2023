#! /usr/bin/env python3

import sys, os
import re

# GLOBALS
LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Find the sum of each valid game ID or the sum of the \"power\" of each minimum viable game.\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def validateGame(game):
    for hint in game.split(";"):
        for color_hint in hint.split(","):
            num, color = color_hint.split()
            if int(num) > LIMITS[color]:
                return False
    return True

def minViableGame(game):
    mins = {"red": 0, "green": 0, "blue": 0}
    for hint in game.split(";"):
        for color_hint in hint.split(","):
            num, color = color_hint.split()
            if int(num) > mins[color]:
                mins[color] = int(num)
    power = 1
    for num in mins.values():
        power *= num
    return power

def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    # Verify valid games based on maximum cube limits
    valid_games = []
    powers = []

    for line in lines:
        x = re.search(r"^Game (\d+):\s+(.*)$", line)
        game_id = int( x.group(1) )
        hint_text = x.group(2)

        if part == 1:
            is_valid = validateGame(hint_text)
            if is_valid:
                valid_games.append(game_id)
        else:
            power = minViableGame(hint_text)
            powers.append(power)
    
    if part == 1:
        print(f"The sum of each calibration value is {sum(valid_games)}")
    else:
        print(f"The sum of the power of each minimum viable game is {sum(powers)}")

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