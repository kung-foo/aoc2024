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
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

machine = {}
machines = []

pos = 10000000000000

for line in src:
    m = re.match(r"Button ([AB]): X\+(\d+), Y\+(\d+)", line)
    if m:
        if m.groups()[0] == "A":
            machine["A"] = [int(x) for x in m.groups()[1:]]
        else:
            machine["B"] = [int(x) for x in m.groups()[1:]]
    else:
        m = re.match(r"Prize: X=(\d+), Y=(\d+)", line)
        machine["P"] = [int(x) for x in m.groups()]
        machine["P"][0] += pos
        machine["P"][1] += pos
        machines.append(machine)
        machine = {}

for m in machines:
    a = np.array([[m["A"][0], m["B"][0]], [m["A"][1], m["B"][1]]])
    b = np.array([[m["P"][0]], [m["P"][1]]])
    x = np.linalg.solve(a, b)

    integer_solution = np.round(x).astype(int)

    if np.all(np.dot(a, integer_solution) == b):
        b1, b2 = integer_solution[:, 0]
        part1 += int(b1 * 3 + b2)


# print("part1:", part1)

print("part2:", part2)
