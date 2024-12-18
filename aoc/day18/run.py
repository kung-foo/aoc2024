#!/usr/bin/env python3

import networkx as nx

# import matplotlib.pyplot as plt

src = open("input.txt", "r").readlines()

example = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
""".splitlines()

# src = example

src = [r.strip() for r in src if r.strip()]

G = nx.Graph()

points = list()

for line in src:
    x, y = line.split(",")
    points.append((int(x), int(y)))

dimx, dimy = 71, 71

for y in range(dimy):
    for x in range(dimx):
        G.add_node((x, y))

        if x < dimx - 1:
            G.add_edge((x, y), (x + 1, y))

        if y < dimy - 1:
            G.add_edge((x, y), (x, y + 1))


exit = (dimx - 1, dimy - 1)
for i, p in enumerate(points):
    G.remove_node(p)

    if i == 1023:
        print("part1:", len(nx.shortest_path(G, (0, 0), exit)) - 1)

    if i > 1023:
        try:
            nx.shortest_path(G, (0, 0), exit)
        except nx.NetworkXNoPath:
            print("part2:", p)
            break

# plt.figure(figsize=(8, 8))
# nx.draw(
#     G,
#     pos={node: node for node in G.nodes},
#     with_labels=True,
# )
# plt.gca().invert_yaxis()
# plt.show()
