#!/usr/bin/env python3

from typing import Generator, List, Set

import numpy as np

src = open("input.txt", "r").readlines()

example = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

dirs = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

arrows = {
    "N": "^",
    "E": ">",
    "S": "v",
    "W": "<",
}

Pos = tuple[int, int]


def step_hash(p: Pos, d: str) -> str:
    return f"{p[1]},{p[0]}-{d}"


def turn(d: str) -> str:
    k = list(dirs.keys())
    return k[(k.index(d) + 1) % len(dirs)]


class Lab:
    src: List[str]
    grid: np.ndarray[str, str]
    start: Pos
    cur: Pos
    dim: int
    dir: str

    def __init__(self, src: list[str]):
        assert len(src) == len(src[0])
        self.src = src
        self.reset()

    def positions(self) -> Generator[Pos, None, None]:
        for y in range(self.grid.shape[0]):
            for x in range(self.grid.shape[1]):
                yield y, x

    def print(self):
        for y in range(self.grid.shape[0]):
            print("".join(self.grid[y, :]))

    def peek(self, d: str = None) -> (str, bool):
        p, ok = self.next_pos(d=d or self.dir)
        if not ok:
            return None, False
        return self.grid[p], True

    def next_pos(self, pos: Pos = None, d: str = None) -> (Pos, bool):
        pos = pos or self.cur
        d = d or self.dir
        p = Pos((pos[0] + dirs[d][0], pos[1] + dirs[d][1]))
        if 0 <= p[0] < self.dim and 0 <= p[1] < self.dim:
            return p, True
        return None, False

    def current_value(self) -> str:
        return self.grid[self.cur]

    def set_value(self, v: str, pos: Pos = None):
        pos = pos or self.cur
        self.grid[pos] = v

    def turn(self):
        self.dir = turn(self.dir)

    def step(self):
        self.cur, _ = self.next_pos()

    def walk(self, mark_path: bool = False) -> (List[str], Set[Pos], bool):
        # path and path set include direction
        path = []
        path_set = set()

        # coordinates only
        visited = set()

        while True:
            visited.add(self.cur)

            v, ok = self.peek()
            if not ok:
                return path, visited, False

            if v == "#":
                self.turn()
                continue

            self.step()

            if mark_path:
                self.set_value("X")

            h = step_hash(self.cur, self.dir)
            if h in path_set:
                return path, visited, True

            path.append(h)
            path_set.add(h)

    def count(self, v: str):
        return np.count_nonzero(self.grid == v)

    def reset(self):
        self.grid = np.stack([np.array(list(l)) for l in self.src])
        self.dim = len(src[0])
        self.dir = "N"

        for pos in self.positions():
            if self.grid[pos] == "^":
                self.start = pos
                self.cur = pos
                self.grid[pos] = "X"
                break


lab = Lab(src)
path, visited, _ = lab.walk(mark_path=True)

if lab.dim == 10:
    assert len(visited) == 41, len(visited)
    assert lab.count("X") == 41, lab.count("X")
    assert path[0] == "4,5-N", path[0]
    assert path[-1] == "7,9-S", path[-1]
else:
    assert lab.count("X") == 4722

print("part1:", lab.count("X"))

lab.reset()

in_front, _ = lab.next_pos(pos=lab.start, d="N")

loops = set()

for p in visited:
    if p in (lab.start, in_front):
        continue

    assert lab.grid[p] == "."

    lab.grid[p] = "#"

    _, _, loop = lab.walk()

    if loop:
        loops.add(p)

    lab.grid[p] = "."
    lab.dir = "N"
    lab.cur = lab.start

print("part2:", len(loops))
