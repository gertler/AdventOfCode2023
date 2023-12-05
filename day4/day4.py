#! /usr/bin/env python3

import sys, os
import re


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Find the sum of the points for each scratchcard.")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()

    points = []
    cards_won = []
    for line in lines:
        x = re.search(r"Card\s+(\d+):(.*)\|(.*)$", line)
        card_num = x.group(1)
        winning = [int(n) for n in x.group(2).strip().split()]
        nums = [int(n) for n in x.group(3).strip().split()]
        matches = 0
        for n in winning:
            if n in nums:
                matches += 1
        cards_won.append(matches)
        points.append(0 if matches == 0 else 1 << (matches - 1))
    
    horde = [1] * len(cards_won)
    if part == 2:
        for i in range(len(cards_won)):
            w = cards_won[i]
            # Increment N times, for each copy in your horde
            num_copies = horde[i]
            horde[i+1:i+1+w] = [ x + num_copies for x in horde[i+1:i+1+w] ]

    if part == 1:
        print(f"The sum of points on every scratchcard is {sum(points)}")
    else:
        print(f"The sum of original scratchcards plus copies is {sum(horde)}")


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