#!/usr/bin/env python3

part1 = 0
part2 = 0

src = open("input.txt", "r").readlines()

example = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

rules = set()

for line in src:
    if "|" in line:
        rules.add(line)


def swap(l: list[str], v1: str, v2: str):
    i1 = l.index(v1)
    i2 = l.index(v2)
    l[i1], l[i2] = v2, v1


for line in src:
    if "|" not in line:
        pages = line.split(",")

        valid = True

        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                if pages[i] + "|" + pages[j] not in rules:
                    valid = False

        if valid:
            part1 += int(pages[len(pages) - 1 >> 1])

        else:
            for i in range(len(pages)):
                for j in range(i + 1, len(pages)):
                    if pages[i] + "|" + pages[j] not in rules:
                        swap(pages, pages[i], pages[j])

            part2 += int(pages[len(pages) - 1 >> 1])

print("part1:", part1)
print("part2:", part2)
