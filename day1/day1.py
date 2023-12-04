#! /usr/bin/env python3

import sys, os

def usage():
    print(f"Usage: {sys.argv[0]} [INPUT FILE]")
    print("Find the sum of each calibration value.\n")
    print("\t-h\tPrint this help message\n")

def main(input_file_name):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    # Collect calibration values
    total = 0
    for line in lines:
        # Calculate first and last digit, then add number to total
        numerals = list( filter( lambda i: i.isnumeric(), line ) )
        first = int( numerals[0] )
        last = int( numerals[-1] )
        num = (first * 10) + last
        total += num
    
    print(f"The sum of each calibration value is {total}")

if __name__ == "__main__":
    # Check args:
    if len(sys.argv) != 2:
        usage()
        exit(1)
    if sys.argv[1] == "-h":
        usage()
        exit(0)
    if not os.path.isfile(sys.argv[1]):
        usage()
        exit(1)
    main(sys.argv[1])