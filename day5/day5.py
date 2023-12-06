#! /usr/bin/env python3

import sys, os
import re


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Discover the lowest location number that maps to any of the given seeds.")
    print("Part 2:\n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


class Range():
    def __init__(self, start, size):
        # Inclusive end
        self.start = start
        self.size = size
        self.mapped = False
        # Inclusive end
        self.end = start + size - 1
    
    def __lt__(self, other):
        return self.start < other.start
    
    def __str__(self) -> str:
        ape = "*" if self.mapped else ""
        return f"{self.start} -> {self.end}{ape}"
    
    def __repr__(self) -> str:
        return self.__str__()

    def setSize(self, newSize):
        self.size = newSize
        self.end = self.start + newSize - 1

    def performMapping(self, dest, src, length):
        # Performing this mapping might split our range, so store those to return
        new_ranges = []

        # No intersection found
        if self.end < src or src + length - 1 < self.start:
            return new_ranges
        
        # Count of outside-map numbers to left/right (0 or negative means range is fully encapsulated)
        left = src - self.start
        right = self.end - (src + length - 1)
        new_size = self.size
        if left > 0:
            new_range = Range(self.start, left)
            new_ranges.append(new_range)
            new_size -= left
            # Update new start in the case that left is splitting
            self.start = src
        if right > 0:
            new_range = Range(self.end - right + 1, right)
            new_ranges.append(new_range)
            new_size -= right

        # Perform mapping
        diff = dest - src
        self.start = self.start + diff
        self.setSize(new_size)
        self.mapped = True

        # Return extra ranges
        return new_ranges



def part1(lines):
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
    
    print(f"The lowest location number that maps to any of the given seeds is {min(map_list)}")


def resetIsMapped(ranges):
    for r in ranges:
        r.mapped = False


def part2(lines):
    # Get initial seed ranges
    x = re.search(r"seeds: (.*)$", lines[0])
    nums = x.group(1).split()
    pairs = [ (nums[i], nums[i+1]) for i in range(0, len(nums), 2) ]
    seeds = [Range(int(st), int(sz)) for st, sz in pairs]

    map_list = [x for x in seeds]
    for line in lines[1:]:
        x = re.search(r"(\d+) (\d+) (\d+)", line)
        if not x:
            # Reset isMapped to False for each range
            # when we reach a new category of mappings
            resetIsMapped(map_list)
            continue
        dest = int(x.group(1))
        src = int(x.group(2))
        length = int(x.group(3))

        i = 0
        check = len(map_list)
        # Loop over each range in our list 
        # (new ranges ignored until next mapping, since new ranges are outside current mapping by definition)
        while i < check:
            curr_range = map_list[i]
            i += 1
            if curr_range.mapped:
                continue
            extra_ranges = curr_range.performMapping(dest, src, length)
            map_list += extra_ranges
    
    print(f"The lowest location number that maps to any of the given seeds is {min(map_list).start}")



def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()

    if part == 1:
        part1(lines)
    else:
        part2(lines)

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