import numpy as np
import matplotlib.pyplot as plt

from src.common import NDArrayFloat


def get_arnoldi_vectors(A: NDArrayFloat, n_iters: int) -> NDArrayFloat:

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    pass


if __name__ == "__main__":
    A = np.array(
        [
            [4.0, 1.0, -1.0, 2.0],
            [1.0, 4.0, 1.0, -1.0],
            [-1.0, 1.0, 4.0, 1.0],
            [2.0, -1.0, 1.0, 1.0],
        ]
    )

    Q = get_arnoldi_vectors(A, n_iters=3)

    ##########################
    ### PUT YOUR CODE HERE ###
    ##########################

    # computing eigenvalues...
