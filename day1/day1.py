#! /usr/bin/env python3

import sys, os
import re

def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Find the sum of each calibration value.\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")

def convert2Int(string):
    helper = {"one": 1, "two": 2, "three": 3, 
              "four": 4, "five": 5, "six": 6, 
              "seven": 7, "eight": 8, "nine": 9}
    result = helper.get(string)
    if not result:
        result = int(string)
    return result

def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    # Collect calibration values
    total = 0
    if part == 1:
        regex1 = r"([0-9])"
        regex2 = r"([0-9])"
    else:
        regex1 = r"(one|two|three|four|five|six|seven|eight|nine|[0-9])"
        regex2 = r"(eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|[0-9])"
    for line in lines:
        # Calculate first and last digit, then add number to total
        first = re.search(regex1, line).group()
        first = convert2Int(first)

        last = re.search(regex2, line[::-1]).group()
        last = convert2Int(last[::-1])

        num = (first * 10) + last
        total += num
    
    print(f"The sum of each calibration value is {total}")

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