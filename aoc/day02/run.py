#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]


def check(row) -> bool:
    r2 = np.delete(row.copy(), 0)
    r1 = np.delete(row, -1)

    d = r1 - r2

    if np.all(d > 0) or np.all(d < 0):
        d = np.abs(d)
        return np.all(d >= 1) and np.all(d <= 3)

    return False


for line in src:
    row = np.array([int(x) for x in line.split()])

    if check(row):
        part1 += 1
        part2 += 1
    else:
        for i in range(len(row)):
            if check(np.delete(row, i)):
                part2 += 1
                break


print("part1:", part1)
print("part2:", part2)
