import numpy as np
import random

# Index, outgoing links
Node = tuple[int, list[int]]

class Network:
    def __init__(self, num_nodes : int, max_links : int = 5) -> None:
        """
        Creates a new network

        num_nodes : Number of nodes in network
        max_links : Maximum number of outgoing links from each node
        """
        
        self.num_nodes = num_nodes
        self.nodes = [self.generate_node(i, num_nodes, max_links) for i in range(num_nodes)]

    def generate_node(self, index : int, num_nodes : int, max_links : int) -> Node:
        """
        Creates a single node

        index : The index of the given node
        num_nodes : Number of nodes in network
        max_links : Maximum number of outgoing links from given node
        """

        links = list({random.randint(0, min(index + 3, num_nodes - 1)) for _ in range(max_links)})
        if index in links: links.remove(index)
        return (index, links)

    def to_matrix(self) -> np.ndarray:
        """
        Returns a matrix representation of the network, as a left/column stochastic matrix
        """
        
        bases = []

        for node in self.nodes:
            row = np.zeros(self.num_nodes)
            row[node[1]] = 1
            if np.isclose(np.sum(row), 0):
                row = np.ones(self.num_nodes)
            bases.append(row / np.sum(row))
        
        return np.array(bases).T

def pagerank(M : np.ndarray, d : float = 0.85, v : np.ndarray = None, max_iterations : int = 100):
    """
    PageRank-algorithm returning a importance-vector of each page/node in a given adjacency matrix.

    M : A left/column stochastic matrix (i.e. a matrix where all columns sum to 1), representing a network.
    d : The damping factor, representing the chance a web-surfer will randomly choose a new page to visit. The damping factor is usually set to 0.85, where 1 is no damping, and 0 is complete ramdomness.
    v : Optional starting importance-vector (importance-vector is a stochastic vector, i.e. all elements sum to 1).
    max_iterations : Optional factor controlling the maximum number of iterations.
    """

    if M.shape[0] != M.shape[1]: raise ValueError("Matrix is not square")
    N = M.shape[0]

    if v is None: v = np.ones(N) / N
    M = d * M + (1 - d) / N

    for _ in range(max_iterations):
        v_next = M.dot(v)
        if np.allclose(v, v_next): break
        v = v_next

    return v
