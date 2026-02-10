# TM1
# Algorithms for calculate parameters


import numpy as np
from model import Imu


def make_pd(A, eps=1e-8):
    A = 0.5 * (A + A.T)
    w, v = np.linalg.eigh(A)
    w = np.maximum(w, eps)
    return v @ np.diag(w) @ v.T



def mnk(r):
    n = len(r)
    phi = np.zeros((n, 10))
    for i in range(n):
        x = r[i][0, 0]
        y = r[i][1, 0]
        z = r[i][2, 0]
        phi[i] = [
            x * x,
            y * y,
            z * z,
            2 * x * y,
            2 * x * z,
            2 * y * z,
            2 * x,
            2 * y,
            2 * z,
            1
        ]
    G = np.ones((n, 1)) * 1
    # theta = np.linalg.inv(phi.T @ phi) @ phi.T @ G
    theta = np.linalg.pinv(phi) @ G
    A = np.array([
        [theta[0, 0], theta[3, 0], theta[4, 0]],
        [theta[3, 0], theta[1, 0], theta[5, 0]],
        [theta[4, 0], theta[5, 0], theta[2, 0]]
    ])
    b = np.array([[theta[6, 0], theta[7, 0], theta[8, 0]]]).T
    eigvals = np.linalg.eigvalsh(A)
    if not np.all(eigvals > 1e-8):
        A = make_pd(A)
        print('hhh')
    M = np.linalg.cholesky(A).T
    
    w0 = np.linalg.solve(M.T, b)
    print(theta[9, 0], w0.T @ w0)
    imu = Imu(M, w0)
    scale_w = imu.raw_to_acc(r[0])
    k = np.sqrt((9.81 ** 2) / (scale_w.T @ scale_w))
    w0 *= k
    M *= k
    return M, w0


def nmnk(r, imu):
    pass

