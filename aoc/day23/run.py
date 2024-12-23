#!/usr/bin/env python3

import networkx as nx

part1 = 0

src = open("input.txt", "r").readlines()

example = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

G = nx.Graph()

tnodes = set()

for line in src:
    n1, n2 = line.split("-")
    G.add_nodes_from((n1, n2))
    G.add_edge(n1, n2)

    if n1.startswith("t"):
        tnodes.add(n1)

    if n2.startswith("t"):
        tnodes.add(n2)

max_clicque = list()

for clicque in nx.enumerate_all_cliques(G):
    if len(clicque) == 3:
        if set(clicque) & tnodes:
            part1 += 1

    if len(clicque) > len(max_clicque):
        max_clicque = clicque

print("part1:", part1)
print("part2:", ",".join(sorted(max_clicque)))
