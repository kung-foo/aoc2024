#!/usr/bin/env python3

import os
import sys
import random
from typing import List, Generator

import numpy as np

src = open("input.txt", "r").readlines()

example = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".splitlines()

# example = """
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########
#
# <^^>>>vv<v>>v<<
# """.splitlines()

# example = """
# #######
# #@OOO.#
# #.O...#
# #.....#
# #.....#
# #.....#
# #######
#
# >>>>vv
# """.splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

Pos = tuple[int, int]  # y, x

dirs = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

arrowMap = {
    "^": "N",
    "v": "S",
    "<": "W",
    ">": "E",
}


def step(d: str, p: Pos) -> Pos:
    return p[0] + dirs[d][0], p[1] + dirs[d][1]


class Warehouse:
    grid: np.ndarray[str, str]
    path: List[str] = []
    pos: Pos

    def __init__(self, src: list[str]):
        wsrc = []

        for line in src:
            if line.startswith("#"):
                wsrc.append(line)
            else:
                for c in line:
                    self.path.append(arrowMap[c])

        self.grid = np.stack([np.array(list(l)) for l in wsrc])

        for p in self.positions():
            if self.grid[p] == "@":
                self.pos = p
                self.grid[p] = "."
                break

    def positions(self) -> Generator[Pos, None, None]:
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                yield y, x

    def print(self):
        assert self.grid[self.pos] == "."
        self.grid[self.pos] = "@"
        for y in range(self.grid.shape[0]):
            print("".join(self.grid[y, :]))
        self.grid[self.pos] = "."

    def peek(self, d: str, p: Pos = None) -> str:
        p = p or self.pos
        return self.grid[step(d, p)]

    def move(self, d: str):
        assert self.peek(d) == "."
        self.pos = step(d, self.pos)

    def push(self, d: str) -> bool:
        assert self.peek(d) == "O"

        boxes_with_space = 0
        p = self.pos

        while True:
            p = step(d, p)
            v = self.grid[p]

            if v == ".":
                break

            if v == "#":
                return False

            boxes_with_space += 1

        assert boxes_with_space > 0

        p = self.pos

        for i in range(boxes_with_space + 1):
            p = step(d, p)
            if i == 0:
                self.grid[p] = "."

        self.grid[p] = "O"

        return True

    def run(self):
        for d in self.path:
            l = self.peek(d)

            if l == "#":
                continue

            elif l == ".":
                self.move(d)

            else:
                assert l == "O"
                if self.push(d):
                    self.move(d)

    def score(self) -> int:
        s = 0
        for p in self.positions():
            if self.grid[p] == "O":
                s += p[0] * 100 + p[1]

        return s


w = Warehouse(src)
w.run()


print("part1:", w.score())
