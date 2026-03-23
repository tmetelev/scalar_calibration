# TM1
# Algorithms for calculate parameters


import numpy as np
from utils.model import Imu
from utils.utils import coefs_to_invert, invert_to_coefs


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


def q_to_M(q):
    M = np.array([
                [q[0, 0], q[3, 0], q[4, 0]],
                [-q[3, 0], q[1, 0], q[5, 0]],
                [-q[4, 0], -q[5, 0], q[2, 0]]
            ])
    w0 = np.array([[q[6, 0], q[7, 0], q[8, 0]]]).T
    return M, w0


def nmnk(r, params):
    iterations = params[0]

    n = len(r)
    q = np.array([[1, 1, 1] + [0] * 9]).T
    G2 = np.ones((n, 1)) * 9.81 * 9.81
    H = np.zeros((n, 12))
    W2 = np.zeros((n, 1))
    imu = Imu()
    for i in range(iterations):
        imu.update_inv(q.T.tolist()[0])
        for j in range(n):
            rx = r[j][0, 0]
            ry = r[j][1, 0]
            rz = r[j][2, 0]
            pW = imu.raw_to_acc(r[j])
            W2[j, 0] = pW.T @ pW
            H[j] = 2 * np.array([pW[0, 0] * rx, pW[1, 0] * ry, pW[2, 0] * rz,
                                 pW[0, 0] * ry, pW[0, 0] * rz,
                                 pW[1, 0] * rx, pW[1, 0] * rz,
                                 pW[2, 0] * rx, pW[2, 0] * ry,
                                 pW[0, 0], pW[1, 0], pW[2, 0]])
        dq = np.linalg.pinv(H) @ (G2 - W2)
        q = q + dq
    return q.T.tolist()[0]


def kalman(raw, R, P0):
    q = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0]]).T
    F = np.diag([1] * 9)
    R = np.array([[200]])
    P = np.diag([])
    G = 9.81 * 9.81
    
    for r in raw:
        q_pred = F @ q
        P_pred = F @ P @ F.T

        M, w0 = q_to_M(q)

        rx = r[0, 0]
        ry = r[1, 0]
        rz = r[2, 0]
        pW = M @ r + w0 
        Y = pW.T @ pW
        H = 2 * np.array([[pW[0, 0] * rx, pW[1, 0] * ry, pW[2, 0] * rz,
                                  pW[0, 0] * ry - pW[1, 0] * rx, pW[0, 0] * rz - pW[2, 0] * rx, -pW[2, 0] * ry + pW[1, 0] * rz,
                                    pW[0, 0], pW[1, 0], pW[2, 0]]])
        
        P = np.linalg.inv(np.linalg.inv(P_pred) + H.T @ np.linalg.inv(R) @ H)
        K = P @ H.T @ np.linalg.inv(R)
        q = q_pred + K @ (G - Y)
    M, w0 = q_to_M(q)
    return M, w0