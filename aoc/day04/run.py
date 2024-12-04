#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

pos = tuple[int, int]

dirs = {
    "N": (0, -1),
    "NE": (1, -1),
    "E": (1, 0),
    "SE": (1, 1),
    "S": (0, 1),
    "SW": (-1, 1),
    "W": (-1, 0),
    "NW": (-1, -1),
}


def load(s: list[str]) -> np.ndarray[str, str]:
    return np.stack([np.array(list(l)) for l in s])


board = load(src)


def word(p: pos, d: str, l: int) -> str:
    w = ""
    for _ in range(l):
        if p[0] < 0 or p[0] >= board.shape[1] or p[1] < 0 or p[1] >= board.shape[0]:
            break

        w += board[p[1], p[0]]

        p = (p[0] + dirs[d][0], p[1] + dirs[d][1])

    return w


def words(p: pos, l: int):
    for d in dirs.keys():
        yield word(p, d, l)


for y in range(board.shape[0]):
    for x in range(board.shape[1]):
        if board[y, x] != "X":
            continue

        for w in words((x, y), 4):
            if w == "XMAS":
                part1 += 1

print("part1:", part1)

for y in range(board.shape[0]):
    for x in range(board.shape[1]):
        w1 = word((x, y), "SE", 3)
        if w1 not in ("MAS", "SAM"):
            continue

        w2 = word((x, y + 2), "NE", 3)
        if w2 not in ("MAS", "SAM"):
            continue

        part2 += 1


print("part2:", part2)
