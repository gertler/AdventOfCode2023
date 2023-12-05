#! /usr/bin/env python3

import sys, os
import re


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Discover the lowest location number that maps to any of the given seeds.")
    print("Part 2:\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()

    # Get initial seeds
    x = re.search(r"seeds: (.*)$", lines[0])
    seeds = [int(s) for s in x.group(1).split()]

    # Loop through mappings
    map_list = [x for x in seeds]
    mapped = [False] * len(seeds)
    for line in lines[1:]:
        x = re.search(r"(\d+) (\d+) (\d+)", line)
        if not x:
            mapped = [False] * len(seeds)
            continue
        dest = int(x.group(1))
        src = int(x.group(2))
        length = int(x.group(3))
        for i in range(len(map_list)):
            num = map_list[i]
            if src <= num < src + length and not mapped[i]:
                diff = dest - src
                map_list[i] = num + diff
                mapped[i] = True
        

    print(map_list)

    if part == 1:
        print(f"The lowest location number that maps to any of the given seeds is {min(map_list)}")
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