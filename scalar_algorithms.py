# TM1
# Algorithms for calculate parameters


import numpy as np
from utils.model import Imu


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
    print(eigvals)
    if not np.all(eigvals > 1e-30):
        print('Calibration Failed: A < 0')
        print()
        return np.zeros((3, 3)), np.zeros((3, 1))
    M = np.linalg.cholesky(A).T
    
    w0 = np.linalg.solve(M.T, b)
    M[1, 0] = M[0, 1]
    M[2, 0] = M[0, 2]
    M[2, 1] = M[1, 2]
    imu = Imu(M, w0)
    scale_w = imu.raw_to_acc(r[0])
    k = np.sqrt((9.81 ** 2) / (scale_w.T @ scale_w))
    w0 *= k
    M *= k
    return M, w0


def test_rotation():
    pass

