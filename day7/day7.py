#! /usr/bin/env python3

import sys, os
import re


def usage():
    print(f"Usage: {sys.argv[0]} -p [PART_NUMBER] [INPUT_FILE]")
    print("Part 1: ")
    print("Part 2: \n")
    print("\t-p\tEither 1 or 2 for the part")
    print("\t-h\tPrint this help message\n")


class CamelHand():
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        freq = {}
        for c in hand:
            freq[c] = 1 if c not in freq else 1 + freq[c]
        self.freq = freq
        self.type = self._handType()
    
    def __lt__(self, other):
        order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        if self.type != other.type:
            return self.type < other.type
        for i in range(len(self.hand)):
            a = self.hand[i]
            b = other.hand[i]
            if a == b:
                continue
            return order.index(a) < order.index(b)
        return False
    
    def __eq__(self, other):
        return self.hand == other.hand
    
    def _handType(self):
        types = {"high": 0, "one": 1, "two": 2, "three": 3, "full": 4, "four": 5, "five": 6}

        if len(self.freq.keys()) == 5:
            self.typeStr = "high card"
            return types["high"]
        elif len(self.freq.keys()) == 1:
            self.typeStr = "five of a kind"
            return types["five"]
        elif 4 in self.freq.values():
            self.typeStr = "four of a kind"
            return types["four"]
        elif len(self.freq.keys()) == 2:
            self.typeStr = "full house"
            return types["full"]
        elif 3 in self.freq.values():
            self.typeStr = "three of a kind"
            return types["three"]
        elif len(self.freq.keys()) == 3:
            self.typeStr = "two pair"
            return types["two"]
        else:
            self.typeStr = "one pair"
            return types["one"]


def main(input_file_name, part):
    lines = []
    # Read lines from input
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    
    camel_hands = []
    for line in lines:
        x = re.search(r"(\w*) (\d+)", line)
        hand = x.group(1)
        bid = int(x.group(2))
        camel = CamelHand(hand, bid)
        camel_hands.append(camel)
    
    camel_hands.sort()

    winnings = 0
    for i in range(len(camel_hands)):
        winnings += (i + 1) * camel_hands[i].bid

    if part == 1:
        print(f"The total winnings are {winnings}")

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