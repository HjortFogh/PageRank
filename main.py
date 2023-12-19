import pagerank as pr

network = pr.Network(5)

for d in [0.0, 0.5, 1.0]:
    rank = pr.pagerank(network.to_matrix(), d)
    print(f"PageRank (d={d}): {rank}")
