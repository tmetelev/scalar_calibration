# TM1
# Reading logs


import numpy as np
import math
# from utils.model import Imu


def log_reader(f_name):
    f = open(f_name)
    n = int(f.readline())
    raw_data = []
    for i in range(n):
        r = np.array([[int(x) for x in f.readline().split()]]).T
        raw_data.append(r)
    return raw_data

def save_imu_config(imu, f_name):
    M, w0 = imu.get_params()
    f = open(f_name, 'w')
    params = [M[0, 0], M[1, 1], M[2, 2], M[0, 1], M[0, 2], M[1, 2], w0[0, 0], w0[1, 0], w0[2, 0]]
    print(' '.join(map(str, params)), file=f)
    f.close()

# def imu_from_config(f_name, noise=0):
#     f = open(f_name)
#     params = [float(x) for x in f.readline().split()]
#     M = np.array([
#         [params[0], params[3], params[4]],
#         [-params[3], params[1], params[5]],
#         [-params[4], -params[5], params[2]]
#     ])
#     w0 = np.array([[params[6], params[7], params[8]]]).T
#     return Imu(M, w0, noise)

def coefs_to_invert(M, F, r0):
    return np.linalg.inv(M @ F), -np.linalg.inv(M @ F) @ r0

def invert_to_coefs(iM, w0):
    MF = np.linalg.inv(iM)
    M = np.diag([MF[0, 0], MF[1, 1], MF[2, 2]])
    F = np.linalg.inv(M) @ MF
    r0 = -M @ F @ w0
    return M, F, r0

def matrices_to_list(M, F, r0):
    return [M[0,0], M[1, 1], M[2, 2],
            F[0, 1], F[0, 2], F[1, 0], F[1, 2], F[2, 0], F[2, 1],
            r0[0, 0], r0[1, 0], r0[2, 0]]

def cartesian_to_spherical(x, y, z):
    r = math.sqrt(x**2 + y**2 + z**2)
    
    # азимут (в плоскости XY)
    theta = math.atan2(y, x)
    
    # полярный угол (от оси Z)
    phi_angle = math.acos(z / r)
    
    return theta, phi_angle

def get_dodecaedr():
    # phi = (1 + math.sqrt(5)) / 2
    # a = 1 / phi
    # b = 1

    # # вершины додекаэдра (стандартная конструкция)
    # vertices = []

    # # (±1, ±1, ±1)
    # for x in [-1, 1]:
    #     for y in [-1, 1]:
    #         for z in [-1, 1]:
    #             vertices.append((x, y, z))

    # # (0, ±1/φ, ±φ)
    # for y in [-a, a]:
    #     for z in [-phi, phi]:
    #         vertices.append((0, y, z))

    # # (±1/φ, ±φ, 0)
    # for x in [-a, a]:
    #     for y in [-phi, phi]:
    #         vertices.append((x, y, 0))

    # # (±φ, 0, ±1/φ)
    # for x in [-phi, phi]:
    #     for z in [-a, a]:
    #         vertices.append((x, 0, z))

    # return [cartesian_to_spherical(x, y, z) for x, y, z in vertices]
    return [(-2.356194490192345, 2.186276035465284), (-2.356194490192345, 0.9553166181245092), (2.356194490192345, 2.186276035465284), (2.356194490192345, 0.9553166181245092), (-0.7853981633974483, 2.186276035465284), (-0.7853981633974483, 0.9553166181245092), (0.7853981633974483, 2.186276035465284), (0.7853981633974483, 0.9553166181245092), (-1.5707963267948966, 2.7767288254763103), (-1.5707963267948966, 0.36486382811348295), (1.5707963267948966, 2.7767288254763103), (1.5707963267948966, 0.36486382811348295), (-1.9356601549083798, 1.5707963267948966), (1.9356601549083798, 1.5707963267948966), (-1.2059324986814135, 1.5707963267948966), (1.2059324986814135, 1.5707963267948966), (3.141592653589793, 1.9356601549083798), (3.141592653589793, 1.2059324986814135), (0.0, 1.9356601549083798), (0.0, 1.2059324986814135)]