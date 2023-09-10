import cli
num_agents, num_iterations, num_nodes = cli.request(["number of agents", int, None], ["number of iterations", int, 100], ["number of nodes", int, 100])

import numpy as np
import pagerank as pr

np.set_printoptions(precision=3)

network = pr.generate_network(num_nodes)
agents = pr.generate_agents(num_agents, num_nodes)

for i in range(num_iterations):
    agents = pr.progess_agents(agents, network)

print("Simulating PageRank algorithm with:")
print(f"   Number of agents     : {num_agents}")
print(f"   Number of iterations : {num_iterations}")
print(f"   Number of nodes      : {num_nodes}\n")

simulated_rank = pr.agent_pagerank(agents, num_iterations)
actual_rank = pr.pagerank(network)

print("Actual rank   :", actual_rank)
print("Simulated rank:", simulated_rank)
