import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def qr(A: NDArrayFloat) -> tuple[NDArrayFloat, NDArrayFloat]:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def get_eigenvalues_via_qr(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def householder_tridiagonalization(A: NDArrayFloat) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


def sign(x):
    return 1 if x > 0 else -1


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 1.0, -1.0, 2.0],
            [1.0, 4.0, 1.0, -1.0],
            [-1.0, 1.0, 4.0, 1.0],
            [2.0, -1.0, 1.0, 1.0],
        ]
    )

    eigvals = get_eigenvalues_via_qr(A, n_iters=20)

    A_tri = householder_tridiagonalization(A)
    eigvals_tri = get_eigenvalues_via_qr(A_tri, n_iters=20)
