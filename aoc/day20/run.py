#!/usr/bin/env python3

from typing import Tuple, Generator, Dict

import numpy as np


src = open("input.txt", "r").readlines()

example = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

dirs = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

flips = [
    [1, 1],
    [-1, 1],
    [1, -1],
    [-1, -1],
]

Pos = Tuple[int, int]  # y, x


def step(d: str, p: Pos, n: int = 1) -> Pos:
    return p[0] + n * dirs[d][0], p[1] + n * dirs[d][1]


class Maze:
    grid: np.ndarray[str, str]
    start: Pos
    end: Pos

    def __init__(self, src: list[str]):
        self.grid = np.stack([np.array(list(l)) for l in src])

        for p in self.positions():
            if self.grid[p] == "S":
                self.start = p
                self.grid[p] = "."

            if self.grid[p] == "E":
                self.end = p
                self.grid[p] = "."

    def positions(self) -> Generator[Pos, None, None]:
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                yield y, x

    def peek(self, d: str, p: Pos) -> str:
        v, _ = self.check(step(d, p))
        return v

    def check(self, p: Pos, expect: str = ".") -> Tuple[str, bool]:
        if 0 <= p[0] < self.grid.shape[0] and 0 <= p[1] < self.grid.shape[1]:
            v = self.grid[p]
            if expect == "" or v == expect:
                return v, True
            return v, False
        return "", False

    def neighbors(
        self, pos: Pos, expect: str = "."
    ) -> Generator[Tuple[str, Pos], None, None]:
        for d in dirs.keys():
            if self.peek(d, pos) == expect:
                yield d, step(d, pos)

    def manhattan(
        self, pos: Pos, d: int = 1, expect: str = "."
    ) -> Generator[Tuple[str, Pos], None, None]:
        seen = set()  # ugh...

        for flip in flips:
            for p in zip(range(0, d + 1), range(d, -1, -1)):
                p1 = (pos[0] + p[0] * flip[0], pos[1] + p[1] * flip[1])
                if p1 in seen:
                    continue
                seen.add(p1)
                v, ok = self.check(p1, expect)
                if ok:
                    yield v, p1

    def walk(self) -> Generator[Pos, None, None]:
        p = self.start
        prev = self.start

        while True:
            yield p

            for n in self.neighbors(p):
                if n[1] != prev:
                    prev = p
                    p = n[1]
                    break

            if p == self.end:
                break

        yield self.end

    def run(self):
        dist: Dict[Pos, int] = {}

        d = 0
        for p in self.walk():
            dist[p] = d
            d += 1

        part1, part2 = 0, 0

        for p1 in self.walk():
            for m in range(2, 21):
                for v, p2 in self.manhattan(p1, m):
                    saved = dist[p2] - dist[p1] - m

                    if saved >= 100:
                        if m == 2:
                            part1 += 1
                        part2 += 1

        print("part1:", part1)
        print("part2:", part2)


m = Maze(src)
m.run()
