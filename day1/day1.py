#! /usr/bin/env python3

import sys, os

def usage():
    print(f"Usage: {sys.argv[0]} [INPUT FILE]")
    print("Find the Elf carrying the most Calories.\n")
    print("\t-h\tPrint this help message\n")

def main():
    pass

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