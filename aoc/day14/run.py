#!/usr/bin/env python3
import math
from PIL import Image

import re


src = open("input.txt", "r").readlines()

example = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".splitlines()


# src = example

src = [r.strip() for r in src if r.strip()]

robots = []

dimX = 101
dimY = 103

for line in src:
    m = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
    px, py, vx, vy = map(int, m.groups())
    robots.append(
        {
            "p": [px, py],
            "v": [vx, vy],
        }
    )


def draw(robots: list, i: int) -> None:
    if i % dimX == 2:
        image = Image.new("RGB", (dimX, dimY))
        for robot in robots:
            px, py = robot["p"]
            image.putpixel((px, py), (0, 255, 0))

        image.save(f"easter-eggs/tree-{i:04}.png")


for i in range(10_000):
    for robot in robots:
        p, v = robot["p"], robot["v"]
        robot["p"] = [p[0] + v[0], p[1] + v[1]]
        robot["p"][0] %= dimX
        robot["p"][1] %= dimY

    draw(robots, i + 1)

    if i + 1 == 100:
        q0, q1, q2, q3 = 0, 0, 0, 0

        for robot in robots:
            p = robot["p"]

            if p[0] == dimX // 2 or p[1] == dimY // 2:
                continue

            if p[0] <= dimX // 2:
                if p[1] <= dimY // 2:
                    q0 += 1
                else:
                    q1 += 1
            else:
                if p[1] <= dimY // 2:
                    q2 += 1
                else:
                    q3 += 1

        print("part1:", math.prod((q0, q1, q2, q3)))
