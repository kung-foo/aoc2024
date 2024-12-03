#!/usr/bin/env python3

import os
import sys
import random
import numpy as np
import re

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))idea
""".splitlines()

example2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".splitlines()

# src = example2

src = [r.strip() for r in src if r.strip()]

enabled = True

for line in src:
    for m in re.findall(r"mul\((\d+),(\d+)\)", line):
        part1 += int(m[0]) * int(m[1])

    for m in re.findall(r"(mul\((\d+),(\d+)\))|(do\(\))|(don\'t\(\))", line):
        if m[3] == "do()":
            enabled = True
        elif m[4] == "don't()":
            enabled = False
        else:
            if enabled:
                part2 += int(m[1]) * int(m[2])


print("part1:", part1)
print("part2:", part2)
