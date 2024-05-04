import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def power_method(A: NDArrayFloat, n_iters: int) -> tuple[NDArrayFloat, NDArrayFloat]:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    V = np.array(
        [
            [1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0],
            [3.0, -1.0, -2.0],
        ]
    )
    dominant_eigenvalue_values = [3.0, 2.1]
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    n_iters = 100
    for e in dominant_eigenvalue_values:
        L = np.diag([e, -2.0, 1.0])
        A = V @ L @ np.linalg.inv(V)
        eigenvalue_history, eigenvector_history = power_method(A, n_iters=n_iters)
        ax.semilogy(
            range(n_iters),
            np.abs(eigenvalue_history - L[0, 0]),
            "o--",
            label=f"Convergence rate: {np.abs(e / L[1, 1])}",
        )
    ax.grid()
    ax.legend(fontsize=12)
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel(r"$|\hat{\lambda} - \lambda|$", fontsize=12)
    plt.show()
