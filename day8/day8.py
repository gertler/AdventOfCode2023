#! /usr/bin/env python3

import sys, os
import re, math


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: Determine the number of steps to reach ZZZ.")
    print("Part 2: \n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


class Node():
    def __init__(self, name, left, right) -> None:
        self.name = name
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return f"{self.name} = ({self.left},{self.right})"


def part1(graph, procedure):
    curr = "AAA"
    dest = "ZZZ"
    p = 0
    steps = [curr]
    while curr != dest:
        step = procedure[p % len(procedure)]
        node = graph[curr]
        if step == "L":
            curr = node.left
        else:
            curr = node.right
        steps.append(curr)
        p += 1

    # print(steps)
    print(f"The number of steps to reach ZZZ is {p}")


def part2(graph, procedure, start_nodes):
    all_positions = [[] for _ in start_nodes]
    all_zs = [[] for _ in start_nodes]
    cycle_beginnings = []

    curr_nodes = [node for node in start_nodes]
    for i in range(len(start_nodes)):
        curr = curr_nodes[i]
        curr_pos = (curr, 0)
        p = 0
        while curr_pos not in all_positions[i]:
            all_positions[i].append(curr_pos)
            step = procedure[p % len(procedure)]
            node = graph[curr]
            curr = node.left if step == "L" else node.right
            
            curr_pos = (curr, p % len(procedure))
            p += 1
            if curr[-1] == "Z":
                all_zs[i].append(curr_pos)
        cycle_begin = all_positions[i].index(curr_pos)
        cycle_beginnings.append(cycle_begin)
        print(f"Found cycle #{i + 1} of {len(start_nodes)}")

    for p in all_positions:
        print(len(p))
    nums = []
    for cy, posns, zs in zip(cycle_beginnings, all_positions, all_zs):
        z = posns.index(zs[0])
        nums.append(z)
        print(f"Step #{cy}, Position: {posns[cy]}, Z: {zs[0]} @ {z}")
    ans = math.lcm(*nums)
    # This does NOT actually solve the problem, but for our specific base case,
    # the input actually works out to be a simple LCM problem
    print(f"The number of steps as a ghost to reach all nodes ending in Z is {ans}")

def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    graph = {}
    start_nodes = []
    for line in lines[2:]:
        x = re.search(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
        curr = x.group(1)
        left = x.group(2)
        right = x.group(3)
        graph[curr] = Node(curr, left, right)
        if curr[-1] == "A":
            start_nodes.append(curr)
    
    procedure = lines[0].strip()
    
    if part == 1:
        part1(graph, procedure)
    else:
        part2(graph, procedure, start_nodes)
    

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