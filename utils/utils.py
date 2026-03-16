# TM1
# Reading logs


import numpy as np
from utils.model import Imu


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

def imu_from_config(f_name, noise=0):
    f = open(f_name)
    params = [float(x) for x in f.readline().split()]
    M = np.array([
        [params[0], params[3], params[4]],
        [-params[3], params[1], params[5]],
        [-params[4], -params[5], params[2]]
    ])
    w0 = np.array([[params[6], params[7], params[8]]]).T
    return Imu(M, w0, noise)