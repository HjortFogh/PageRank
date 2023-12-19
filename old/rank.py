import cli
num_nodes, num_iterations, damping_factor = cli.request(["number of nodes", int, None], ["number of iterations", int, 100], ["damping factor", float, 0.85])

import numpy as np
from pagerank import generate_network, pagerank

np.set_printoptions(precision=3)

print("Calculating PageRank algorithm with:")
print(f"   Number of nodes      : {num_nodes}")
print(f"   Number of iterations : {num_iterations}")
print(f"   Damping factor       : {damping_factor}\n")

network = generate_network(num_nodes)
rank = pagerank(network, num_iterations, damping_factor)

print("PageRank:", rank)
