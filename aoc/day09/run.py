#!/usr/bin/env python3
import collections
import os
import sys
import random
import numpy as np

src = open("input.txt", "r").read()

example = "2333133121414131402"
# example = "12345"

# src = example


def print_disk():
    for c in disk:
        if c == -1:
            print(".", end="")
        else:
            print(c, end="")
    print()


def checksum() -> int:
    s = 0
    for i, c in enumerate(disk):
        if c == -1:
            continue
        s += i * c
    return s


def init_disk(src: str):
    disk_size = sum(map(int, list(src.strip())))
    src = map(int, list(src.strip()))

    sz = 0
    lens = collections.OrderedDict()
    pos = 0
    file_positions = {}

    disk = [-1] * disk_size

    for i, c in enumerate(src):
        if i % 2 == 0:
            file_id = i >> 1
            lens[file_id] = c
            sz += c
            if file_id not in file_positions:
                file_positions[file_id] = pos
            for x in range(c):
                disk[pos] = file_id
                pos += 1
        else:
            pos += c

    return disk, sz, lens, file_positions


disk, total_file_sz, _, _ = init_disk(src)

free_space_ptr = disk.index(-1)

for i, c in enumerate(disk[::-1]):
    if c == -1:
        continue
    if len(disk) - i - 1 < total_file_sz:
        break

    disk[free_space_ptr] = c
    disk[len(disk) - 1 - i] = -1

    free_space_ptr = disk.index(-1, free_space_ptr + 1)


# print_disk()
print("part1:", checksum())

disk, total_file_sz, file_lengths, file_positions = init_disk(src)


def find_block(disk: list[int], sz: int) -> int:
    start = 0

    try:
        while True:
            pos = disk.index(-1, start)
            chunk_sz = 0

            start = pos

            while disk[pos] == -1:
                chunk_sz += 1
                pos += 1

                if chunk_sz == sz:
                    return start

                if pos >= len(disk):
                    return -1

            while disk[pos] != -1:
                pos += 1

            start = pos
    except:
        return -1


for f in reversed(file_lengths.items()):
    fid, sz = f
    block_pos = find_block(disk, sz)
    if block_pos == -1:
        continue

    orig_pos = file_positions[fid]
    if orig_pos == 0 or block_pos >= orig_pos:
        continue

    for i in range(sz):
        disk[block_pos + i] = fid
        disk[orig_pos + i] = -1


print("part2:", checksum())
