#! /usr/bin/env python3

import sys, os
import re


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
    curr = start_nodes
    dest = lambda n: n[-1] == "Z"
    def next_map(st, node):
        return node.left if st == "L" else node.right
    p = 0
    while not all(map(dest, curr)):
        index = p % len(procedure)
        step = procedure[index]
        nodes = (graph[c] for c in curr)
        curr = [next_map(step, node) for node in nodes]
        p += 1
        print(curr)

    print(f"The number of steps as a ghost to reach all nodes ending in Z is {p}")

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