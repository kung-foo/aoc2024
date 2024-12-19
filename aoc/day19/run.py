#!/usr/bin/env python3

from functools import cache

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

patterns = src.pop(0).split(", ")


@cache
def check(towelie: str) -> int:
    perm = 0

    for p in patterns:
        if towelie == p:
            perm += 1

        if towelie.startswith(p):
            perm += check(towelie[len(p) :])

    return perm


for line in src:
    c = check(line)
    if c > 0:
        part1 += 1
    part2 += c

print("part1:", part1)
print("part2:", part2)
