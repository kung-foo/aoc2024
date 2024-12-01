#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
from collections import defaultdict

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
3   4
4   3
2   5
1   3
3   9
3   3
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

left = list()
right = list()

for line in src:
    x, y = line.split()
    left.append(int(x))
    right.append(int(y))


left.sort()
right.sort()

counts = defaultdict(int)

for i in range(len(left)):
    part1 += abs(left[i] - right[i])
    counts[right[i]] += 1

print("part1:", part1)

for i in range(len(left)):
    part2 += left[i] * counts[left[i]]

print("part2:", part2)
