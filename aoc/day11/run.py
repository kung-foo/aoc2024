#!/usr/bin/env python3

import math
from functools import cache

part1 = 0
part2 = 0

src = open("input.txt", "r").read().strip()

example = "125 17"

# src = example

src = [int(x) for x in src.split(" ")]


@cache
def stones(s: int, d: int) -> int:
    if d == 0:
        return 1

    if s == 0:
        return stones(1, d - 1)

    if (math.floor(math.log10(s)) + 1) % 2 == 0:
        s0 = str(s)
        s1 = s0[: len(s0) >> 1]
        s2 = s0[len(s0) >> 1 :]

        return stones(int(s1), d - 1) + stones(int(s2), d - 1)

    return stones(s * 2024, d - 1)


for stone in src:
    part1 += stones(stone, 25)
    part2 += stones(stone, 75)

print("part1:", part1)
print("part2:", part2)
