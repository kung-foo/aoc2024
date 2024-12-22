#!/usr/bin/env python3

import os
import sys
import random
from typing import Set, Tuple, Dict

import numpy as np

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
1
2
3
2024
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]


def banana(
    seed: int, rounds: int
) -> (int, Set[Tuple[int, int, int, int]], Dict[Tuple[int, int, int, int], int]):
    prices = []

    change_set = set()
    max_bananas = {}

    for i in range(rounds):
        price = seed % 10
        prices.append(price)

        seed = seed ^ (seed << 6)
        seed %= 16_777_216

        seed = seed ^ (seed >> 5)
        seed %= 16_777_216

        seed = seed ^ (seed << 11)
        seed %= 16_777_216

        if i > 3:  # 🍌🍌🍌🍌
            changes = (
                prices[1] - prices[0],
                prices[2] - prices[1],
                prices[3] - prices[2],
                prices[4] - prices[3],
            )

            prices.pop(0)  # -= 🍌

            if changes in change_set:
                continue  # 🍌 GTFO

            change_set.add(changes)  # += 🍌
            max_bananas[changes] = price

    return seed, change_set, max_bananas


all_change_sets = set()  # 🍌
bananas_bananas = []  # 🍌

for line in src:
    seed, change_set, bananas = banana(int(line), 2000)  # 🍌
    all_change_sets.update(change_set)  # 🍌
    bananas_bananas.append(bananas)  # 🍌
    part1 += seed  # 🍌

max_bananas = 0  # 🍌

for cs in all_change_sets:
    maybe_max_bananas = 0  # 🍌

    for bananas in bananas_bananas:
        maybe_max_bananas += bananas.get(cs, 0)  # 🍌

    max_bananas = max(max_bananas, maybe_max_bananas)  # 🍌

print("part1 🍌:", part1)
print("part2 🍌:", max_bananas)
