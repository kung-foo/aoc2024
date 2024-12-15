#!/usr/bin/env python3

import os
import sys
import random
from typing import List, Generator, Set, Tuple

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
# #.....#
# #.....#
# #..OO@#
# #.....#
# #.....#
# #######
#
# <<
# """.splitlines()
#
# example = """
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######
#
# <vv<<^^<<^^
# """.splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

Pos = Tuple[int, int]  # y, x
Box = Tuple[Pos, Pos]

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


def step(d: str, p: Pos, n: int = 1) -> Pos:
    return p[0] + n * dirs[d][0], p[1] + n * dirs[d][1]


class Warehouse:
    grid: np.ndarray[str, str]
    path: List[str] = []
    pos: Pos

    def __init__(self, src: list[str]):
        wsrc = []

        for line in src:
            if line.startswith("#"):
                wsrc.append(
                    line.replace("#", "##")
                    .replace(".", "..")
                    .replace("@", "@.")
                    .replace("O", "[]")
                )
            else:
                for c in line:
                    self.path.append(arrowMap[c])

        self.grid = np.stack([np.array(list(l)) for l in wsrc])

        for p in self.positions():
            if self.grid[p] == "@":
                self.pos = p
                self.grid[p] = "."
                break

    def is_box(self, p: Pos) -> bool:
        return self.grid[p] in "[]"

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

    def expand_box(self, box_p: Pos) -> Box:
        if self.grid[box_p] == "[":
            return box_p, step("E", box_p)
        else:
            return step("W", box_p), box_p

    def slide_slide_slippity_slide(self, box_p: Pos, d: str) -> (bool, Set[Box]):
        assert self.is_box(box_p)

        box = self.expand_box(box_p)

        touching = {box}

        if d in "NS":
            for p in box:
                v = self.peek(d, p)

                if v == "#":
                    return False, None

                if v in "[]":
                    ok, more = self.slide_slide_slippity_slide(step(d, p), d)
                    if not ok:
                        return False, None

                    touching.update(more)

        else:
            if d == "E":
                anchor = 1
            else:
                anchor = 0

            v = self.peek(d, box[anchor])

            if v == "#":
                return False, None

            if v in "[]":
                ok, more = self.slide_slide_slippity_slide(step(d, box[anchor]), d)
                if not ok:
                    return False, None

                touching.update(more)

        return True, touching

    def run(self):
        for i, d in enumerate(self.path):
            l = self.peek(d)

            if l == "#":
                continue

            elif l == ".":
                self.move(d)

            else:
                assert l in "[]"

                can_move, touching = self.slide_slide_slippity_slide(
                    step(d, self.pos), d
                )

                if not can_move:
                    continue

                for box in touching:
                    self.grid[box[0]] = "."
                    self.grid[box[1]] = "."

                for box in touching:
                    self.grid[step(d, box[0])] = "["
                    self.grid[step(d, box[1])] = "]"

                self.move(d)

    def score(self) -> int:
        s = 0
        for p in self.positions():
            if self.grid[p] == "[":
                s += p[0] * 100 + p[1]

        return s


w = Warehouse(src)
w.run()


print("part2:", w.score())
