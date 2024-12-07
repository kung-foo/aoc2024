#!/usr/bin/env python3
import itertools
import math

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

equation = tuple[int, list[int]]

equations: list[equation] = []

for line in src:
    t1, t2 = line.split(": ")
    target = int(t1)
    operands = list(map(int, t2.split()))

    equations.append((target, operands))


def eval(eq: equation, operands: list[str]) -> bool:
    t = eq[1][0]

    for i, op in enumerate(operands):
        if op == "+":
            t += eq[1][i + 1]
        elif op == "*":
            t *= eq[1][i + 1]
        else:
            t = int(str(t) + str(eq[1][i + 1]))

        if t > eq[0]:
            return False

    return t == eq[0]


for eq in equations:
    for operators in itertools.product(["+", "*"], repeat=len(eq[1]) - 1):
        if eval(eq, operators):
            part1 += eq[0]
            break

    for operators in itertools.product(["+", "*", "||"], repeat=len(eq[1]) - 1):
        if eval(eq, operators):
            part2 += eq[0]
            break


print("part1:", part1)
print("part2:", part2)
