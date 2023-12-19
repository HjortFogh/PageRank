# Problems: FIXME:
#    When a node does not link to any other nodes, importance vector will converge towards 0
#    5x5 [[2, 3], [0, 3], [1, 3, 4], [1], [1, 2]] -> converge towards 0

import numpy as np
import random
from typing import Tuple, List

# Node index, link indices
Node = Tuple[int, List[int]]
Network = List[Node]

# Starting index, indices register
Agent = Tuple[int, np.ndarray]

# Explanation ... TODO:FIXME:
DEFAULT_DAMPING = 0.85

def generate_node(index : int, num_nodes : int, max_connections : int = 3) -> Node:
    """Generates a single node, with a random number of links to other nodes"""
    num_links = random.randint(1, min(num_nodes - 1, max_connections))
    max_index = min(num_nodes, num_links * 2)
    
    indices = [i for i in range(max_index) if i != index]
    links = random.sample(indices, num_links)

    return (index, links)

def generate_network(num_nodes : int) -> Network:
    """Generates a network of nodes"""
    return [generate_node(i, num_nodes) for i in range(num_nodes)]

def link_matrix_from_network(network : Network) -> np.ndarray:
    """Creates a link matrix from a network"""
    num_dimensions = len(network)
    vectors = []

    for _, node_links in network:
        vec = np.zeros(num_dimensions, dtype="float64")
        for link in node_links: vec[link] = 1
        vectors.append(vec / np.sum(vec))
    
    return np.stack(vectors, axis=1)

def pagerank(network : Network, num_iterations : int = 100, damping : float = DEFAULT_DAMPING) -> np.ndarray:
    """Ranks a network over 'num_iterations' iterations, and returns the ranks as a vector"""
    num_dimensions = len(network)
    link_matrix = link_matrix_from_network(network)
    
    importance_vector = np.ones(num_dimensions) / num_dimensions
    dampened_link_matrix = damping * link_matrix + (1 - damping) / num_dimensions

    for _ in range(num_iterations):
        importance_vector = dampened_link_matrix @ importance_vector
        
    return importance_vector

def generate_agents(num_agents : int, num_nodes : int) -> List[Agent]:
    """Generates an array of agents"""
    return [(random.randint(0, num_nodes - 1), np.zeros(num_nodes, dtype="int32")) for i in range(num_agents)]

def progess_agent(agent : Agent, network : Network, damping : float) -> Agent:
    """Updates a single agent, eg. moves the agent to an adjacent or random node"""
    last_index, register = agent

    if random.random() > damping:
        next_index = random.choice(network)[0]
    else:
        _, node_links = network[last_index]
        next_index = random.choice(node_links)

    register[next_index] += 1
    return (next_index, register)

def progess_agents(agents : List[Agent], network : Network, damping : float = DEFAULT_DAMPING) -> List[Agent]:
    """Moves all agents"""
    return [progess_agent(agent, network, damping) for agent in agents]

def agent_pagerank(agents : List[Agent], num_iterations : int) -> np.ndarray:
    """Calculates the  rank, based on all the nodes the agents have visited"""
    num_nodes = agents[0][1].shape[0]
    importance = np.zeros(num_nodes, dtype="float64")

    for _, register in agents:
        importance += register
    
    return importance / (len(agents) * num_iterations)
