#!/usr/bin/env python3

import sys
import os.path
import subprocess
from requests import session
from bs4 import BeautifulSoup
import pendulum

year = 2024
day = int(sys.argv[1])

dir = os.path.join("aoc", f"day{day:02}")
os.makedirs(dir)

s = session()
s.cookies["session"] = os.getenv("AOC_SESSION")

r = s.get(f"https://adventofcode.com/{year}/day/{day}")
soup = BeautifulSoup(r.text, features="html.parser")

example = "no idea"

for code in soup.find_all("code"):
    if code.text.count("\n") >= 5:
        example = code.text.strip()
        break

r = s.get(f"https://adventofcode.com/{year}/day/{day}/input")

open(os.path.join(dir, "input.txt"), "w").write(r.text)

src = f'''#!/usr/bin/env python3

import os
import sys
import random
import numpy as np

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
{example}
""".splitlines()

src = example

src = [r.strip() for r in src if r.strip()]

print("part1:", part1)


# print("part2:", part2)

'''

runpy = os.path.join(dir, "run.py")

open(runpy, "w").write(src)

subprocess.run(["chmod", "+x", runpy])

open(os.path.join(dir, ".start"), "w").write(pendulum.now().to_iso8601_string())
