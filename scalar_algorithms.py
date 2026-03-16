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
    G = np.ones((n, 1)) * 9.81
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
    M[1, 0] = -M[0, 1]
    M[2, 0] = -M[0, 2]
    M[2, 1] = -M[1, 2]
    imu = Imu(M, w0)
    scale_w = imu.raw_to_acc(r[0])
    k = np.sqrt((9.81 ** 2) / (scale_w.T @ scale_w))
    w0 *= k
    M *= k
    return M, w0


def nmnk(r, iterations=10):
    n = len(r)
    q = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0]]).T
    G2 = np.ones((n, 1)) * 9.81 * 9.81
    H = np.zeros((n, 9))
    W2 = np.zeros((n, 1))
    M = np.zeros((3, 3))
    w0 = np.zeros((3, 1))
    for i in range(iterations):
        M = np.array([
                [q[0, 0], q[3, 0], q[4, 0]],
                [-q[3, 0], q[1, 0], q[5, 0]],
                [-q[4, 0], -q[5, 0], q[2, 0]]
            ])
        w0 = np.array([[q[6, 0], q[7, 0], q[8, 0]]]).T
        for j in range(n):
            rx = r[j][0, 0]
            ry = r[j][1, 0]
            rz = r[j][2, 0]
            pW = M @ r[j] + w0 
            W2[j, 0] = pW.T @ pW
            H[j] = 2 * np.array([pW[0, 0] * rx, pW[1, 0] * ry, pW[2, 0] * rz,
                                  pW[0, 0] * ry + pW[1, 0] * rx, pW[0, 0] * rz + pW[2, 0] * rx, pW[2, 0] * ry + pW[1, 0] * rz,
                                    pW[0, 0], pW[1, 0], pW[2, 0]])
        dq = np.linalg.pinv(H) @ (G2 - W2)
        q = q + dq
    return M, w0

