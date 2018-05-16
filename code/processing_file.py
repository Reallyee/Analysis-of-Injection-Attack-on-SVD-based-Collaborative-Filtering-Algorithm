import read_file
from numpy import linalg as la
import numpy as np



def singular_value_decomposition():
    print("--------Start SVD----------")
    information = read_file.read_files()
    U, Sigma, Vt = la.svd(np.matrix(information[0]), full_matrices=False)
    p = U
    q = np.dot(np.diag(Sigma), Vt)
    rank = la.matrix_rank(information[0])
    # print("The rank of the initial matrix is:", la.matrix_rank(information[0]))
    # print(p.shape)
    # print(q.shape)
    np.transpose(information[0])
    rank = la.matrix_rank(information[0])
    print(rank)
    return p, q, rank

singular_value_decomposition()








