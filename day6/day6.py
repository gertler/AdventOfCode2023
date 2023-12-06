#! /usr/bin/env python3

import sys, os
import re


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Determines the number of ways you can beat the record in each race.")
    print("Part 2:\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def part1(lines):
    # Get initial seeds
    x = re.search(r"seeds: (.*)$", lines[0])
    seeds = [int(s) for s in x.group(1).split()]
    
    print(f"The lowest location number that maps to any of the given seeds is {""}")


def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()

    if part == 1:
        part1(lines)
    else:
        pass

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