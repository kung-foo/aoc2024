#!/usr/bin/env python3

import os
import sys
import random
from typing import List, Generator, Set

import numpy as np

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

Pos = tuple[int, int]  # y, x


class Map:
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

    def is_valid(self, p: Pos) -> bool:
        return 0 <= p[0] < self.dim and 0 <= p[1] < self.dim

    def trailheads(self) -> Generator[Pos, None, None]:
        for pos in self.positions():
            if self.grid[pos] == "0":
                yield pos

    def neighbors(self, p: Pos) -> Generator[Pos, None, None]:
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            np = p[0] + dy, p[1] + dx
            if self.is_valid(np):
                yield np

    def explore(self, cur: Pos) -> (Set[Pos], int):
        v = self.grid[cur]
        if v == "9":
            return {cur}, 1

        s = set()
        c = 0

        for p in self.neighbors(cur):
            if self.grid[p] == chr(ord(v) + 1):
                s0, c0 = self.explore(p)
                s.update(s0)
                c += c0

        return s, c


m = Map(src)
# m.print()

for th in m.trailheads():
    s, c = m.explore(th)
    part1 += len(s)
    part2 += c

print("part1:", part1)
print("part2:", part2)


# print("part2:", part2)
