#! /usr/bin/env python3

import sys, os
import re


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Determine the sum of each extrapolated value from each history.")
    print("Part 2: Determine the sum of each extrapolated value, going backwards.\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    sums = []
    sums2 = []
    for line in lines:
        vals = map( int, line.strip().split() )
        diffs = [list(vals)]
        while True:
            curr = diffs[-1]
            diff = [curr[i+1] - curr[i] for i in range(len(curr) - 1)]
            diffs.append(diff)
            if len(set(diff)) == 1:
                break
    
        s = sum(x[-1] for x in diffs)
        s2 = 0
        for diff in diffs[::-1]:
            s2 = diff[0] - s2
        sums2.append(s2)
        sums.append(s)

    if part == 1:
        print(f"The sum of the extrapolated values is {sum(sums)}")
    else:
        print(f"The sum of the extrapolated values is {sum(sums2)}")


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