import read_file
from numpy import linalg as la
import numpy as np



def singular_value_decomposition():
    print("--------Start SVD----------")
    information, mean = read_file.read_files()
    U, Sigma, Vt = la.svd(np.matrix(information[0]), full_matrices=False)
    p = U
    q = np.dot(np.diag(Sigma), Vt)
    rank = la.matrix_rank(information[0])
    # print("The rank of the initial matrix is:", la.matrix_rank(information[0]))
    # print(p.shape)
    # print(q.shape)
    return p, q, rank


def train():
    information, mean = read_file.read_files()
    









