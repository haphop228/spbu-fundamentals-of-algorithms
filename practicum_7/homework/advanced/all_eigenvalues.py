from collections import defaultdict
from dataclasses import dataclass
import os
import yaml
import time

import numpy as np
import scipy.io
import scipy.linalg

from src.common import NDArrayFloat
from src.linalg import get_numpy_eigenvalues


@dataclass
class Performance:
    time: float = 0.0
    relative_error: float = 0.0

def qr(A: np.array):
    n = A.shape[0]
    Q = A.copy() # Ortogonal matrice
    R = np.zeros((n, n)) # Upper triangle matrice

    for k in range(n): 
        R[k, k] = np.linalg.norm(Q[:, k])
        Q[:, k] /= R[k, k] 
        for j in range(k + 1, n):  
            R[k, j] = np.dot(Q[:, k], Q[:, j])
            Q[:, j] -= R[k, j] * Q[:, k] 
    return Q, R


def get_all_eigenvalues(A: NDArrayFloat) -> NDArrayFloat:
    A_k = A.copy()
    for k in range(100):
        Q, R = qr(A_k)
        A_k = R @ Q
        
    A_k = np.diag(A_k)
    eigvals = np.array(A_k)
    return eigvals

def run_test_cases(
    path_to_homework: str, path_to_matrices: str
) -> dict[str, Performance]:
    matrix_filenames = []
    performance_by_matrix = defaultdict(Performance)
    with open(os.path.join(path_to_homework, "matrices.yaml"), "r") as f:
        matrix_filenames = yaml.safe_load(f)
    for i, matrix_filename in enumerate(matrix_filenames):
        print(f"Processing matrix {i+1} out of {len(matrix_filenames)}")
        A = scipy.io.mmread(os.path.join(path_to_matrices, matrix_filename)).todense().A
        perf = performance_by_matrix[matrix_filename]
        t1 = time.time()
        eigvals = get_all_eigenvalues(A)
        eigvals_exact = get_numpy_eigenvalues(A)
        t2 = time.time()
        perf.time += t2 - t1
        eigvals_exact.sort()
        eigvals_sort = eigvals.copy()
        eigvals_sort.sort()
        perf.relative_error = np.median(
            np.abs(eigvals_exact - eigvals_sort) / np.abs(eigvals_exact)
        )
    return performance_by_matrix


if __name__ == "__main__":
    path_to_homework = os.path.join("practicum_7", "homework", "advanced")
    path_to_matrices = os.path.join("practicum_6", "homework", "advanced", "matrices")
    performance_by_matrix = run_test_cases(
        path_to_homework=path_to_homework,
        path_to_matrices=path_to_matrices,
    )
    print("\nResult summary:")
    for filename, perf in performance_by_matrix.items():
        print(
            f"Matrix: {filename}. "
            f"Average time: {perf.time:.2e} seconds.  "
            f"Relative error: {perf.relative_error:.2e}"
        )

