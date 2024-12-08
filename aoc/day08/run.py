#!/usr/bin/env python3
import itertools
import os
import sys
import random
from typing import List, Generator, Set, Dict

import numpy as np

src = open("input.txt", "r").readlines()

example = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".splitlines()

example = """
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

Pos = tuple[int, int]  # y, x


class Lab:
    src: List[str]
    grid: np.ndarray[str, str]
    dim: int

    def __init__(self, src: list[str]):
        assert len(src) == len(src[0])
        self.src = src
        self.grid = np.stack([np.array(list(l)) for l in self.src])
        self.dim = len(src[0])

    def positions(self) -> Generator[Pos, None, None]:
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                yield y, x

    def print(self):
        for y in range(self.grid.shape[0]):
            print("".join(self.grid[y, :]))

    def get_antennas(self) -> Dict[str, List[Pos]]:
        antennas = {}

        for p in self.positions():
            a = self.grid[p]
            if a == ".":
                continue

            if a in antennas:
                antennas[a].append(p)
            else:
                antennas[a] = [p]

        return antennas

    def is_valid(self, p: Pos) -> bool:
        return 0 <= p[0] < self.dim and 0 <= p[1] < self.dim

    def find_antinodes(self, mark: bool = False, harmonics: bool = False) -> Set[Pos]:
        antinodes = set()

        antennas = self.get_antennas()

        for k, v in antennas.items():
            if len(v) == 1:
                continue

            for pair in itertools.combinations(v, 2):
                a1, a2 = pair

                if harmonics:
                    antinodes.add(a1)
                    antinodes.add(a2)

                dy1 = a1[0] - a2[0]
                dx1 = a1[1] - a2[1]

                i = 1
                while True:
                    an1 = a1[0] + (i * dy1), a1[1] + (i * dx1)

                    if self.is_valid(an1):
                        antinodes.add(an1)
                        if mark:
                            self.grid[an1] = "#"
                    else:
                        break

                    if not harmonics:
                        break

                    i += 1

                dy2 = a2[0] - a1[0]
                dx2 = a2[1] - a1[1]

                i = 1
                while True:
                    an2 = a2[0] + (i * dy2), a2[1] + (i * dx2)

                    if self.is_valid(an2):
                        antinodes.add(an2)
                        if mark:
                            self.grid[an2] = "#"
                    else:
                        break

                    if not harmonics:
                        break

                    i += 1

        return antinodes


lab = Lab(src)

part1 = len(lab.find_antinodes())

if lab.dim == 12:
    assert part1 == 14, part1

print("part1:", part1)

part2 = len(lab.find_antinodes(mark=True, harmonics=True))

lab.print()

print("part2:", part2)
