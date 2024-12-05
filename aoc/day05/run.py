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

mid = lambda p: int(p[len(p) - 1 >> 1])
has_rule = lambda p, i, j: p[i] + "|" + p[j] not in rules

for line in src:
    if "|" not in line:
        pages = line.split(",")

        valid = True

        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                if has_rule(pages, i, j):
                    valid = False

        if valid:
            part1 += mid(pages)

        else:
            for i in range(len(pages)):
                for j in range(i + 1, len(pages)):
                    if has_rule(pages, i, j):
                        pages[i], pages[j] = pages[j], pages[i]  # swapper-roo

            part2 += mid(pages)

print("part1:", part1)
print("part2:", part2)
