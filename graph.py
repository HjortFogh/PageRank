import pagerank as pr
import numpy as np
import matplotlib.pyplot as plt
import time

def perf_timer(func, n, stdout = True, args = []):
    t0 = time.process_time_ns()
    
    for i in range(n):
        if not func(*args):
            raise Exception(f"Aborting performance timer for {func.__name__} (loop: {i})")
            
    elapsed_time = time.process_time_ns() - t0
    if (stdout):
        print(f"Elapsed time (function: {func.__name__}, n: {n}): {elapsed_time:.2f} ns (approx {elapsed_time / 1000000000:.2f} s)")

    return elapsed_time

def pagerank_bruteforce(link_matrix, rank):
    v = pr.pagerank(link_matrix, d=1)
    return np.allclose(v, rank, atol=1e-5)

def pagerank_eigenvector(link_matrix, rank):
    eigenvalues, eigenvectors = np.linalg.eig(link_matrix)
    index = np.where(np.isclose(eigenvalues, 1))[0][0]
    v = eigenvectors[:, index] / np.sum(eigenvectors[:, index])
    return np.allclose(v, rank, atol=1e-5)

start, stop, step = 2, 200, 20
num_nodes = np.linspace(start, stop, (stop - start + 1) // step, dtype="int")

bruteforce_data = [0 for _ in range((stop - start + 1) // step)]
eigenvector_data = [0 for _ in range((stop - start + 1) // step)]

num_calls = 50

for i, n in enumerate(num_nodes):
    print("---", n)
    for j in range(3):
        link_matrix = pr.Network(n).to_matrix()
        link_matrix = 0.85 * link_matrix + 0.15 / n

        rank = pr.pagerank(link_matrix, d=1)
        
        bruteforce_data[i] += perf_timer(pagerank_bruteforce, n=num_calls, stdout=False, args=[link_matrix, rank])
        eigenvector_data[i] += perf_timer(pagerank_eigenvector, n=num_calls, stdout=False, args=[link_matrix, rank])

plt.plot(num_nodes, bruteforce_data, c="r", label="Bruteforce")
plt.plot(num_nodes, eigenvector_data, c="b", label="Eigenvector")

plt.ylabel("Tid i nanosekunder")
plt.xlabel("Størrelse af reference-matrix")

plt.legend(loc="upper left")
plt.show()