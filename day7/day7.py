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
    def __init__(self, hand, bid, part):
        # Adding part here so hand type and comparisons can be done with Jokers in part 2
        self.part = part

        self.hand = hand
        self.bid = bid
        freq = {}
        for c in hand:
            freq[c] = 1 if c not in freq else 1 + freq[c]
        self.freq = freq
        self.type = self._handType()
    
    def __lt__(self, other):
        # Card strength, based on whether Jokers exist or not
        order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
        if self.part == 1:
            order.insert(9, "J")
        else:
            order.insert(0, "J")
        
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
    
    def __repr__(self) -> str:
        types = ["high card", "one pair", "two pair", "three of a kind", "full house", "four of a kind", "five of a kind"]
        return f"{self.hand}, {types[self.type]}"
    
    def _handType(self):
        types = {"high": 0, "one": 1, "two": 2, "three": 3, "full": 4, "four": 5, "five": 6}

        has_jokers = False
        jokers_count = 0
        if self.part == 2 and "J" in self.freq.keys():
            jokers_count = self.freq["J"]
            has_jokers = jokers_count > 0

        result = 0

        if len(self.freq.keys()) == 5:
            result = types["one"] if has_jokers else types["high"]
        elif len(self.freq.keys()) == 1:
            result = types["five"]
        elif 4 in self.freq.values():
            result = types["five"] if has_jokers else types["four"]
        elif len(self.freq.keys()) == 2:
            result = types["five"] if has_jokers else types["full"]
        elif 3 in self.freq.values():
            result = types["four"] if has_jokers else types["three"]
        elif len(self.freq.keys()) == 3:
            result = types["two"]
            if jokers_count == 1:
                result = types["full"]
            elif jokers_count == 2:
                result = types["four"]
        else:
            result = types["three"] if has_jokers else types["one"]
        
        return result


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
        camel = CamelHand(hand, bid, part)
        camel_hands.append(camel)
    
    camel_hands.sort()

    winnings = 0
    for i in range(len(camel_hands)):
        winnings += (i + 1) * camel_hands[i].bid

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