# TM1
# Model of IMU sensor


import numpy as np
from utils.utils import coefs_to_invert, invert_to_coefs


G = 9.81


class Imu():
    def __init__(self, params=[1] * 3 + [0] * 9, noise=0):
        self.M = None
        self.F = None
        self.r0 = None
        self.update(params)
        self.__noise = noise

    def generate_rotation(self, v_points=5, h_points=9):
        res = []
        for phi in np.linspace(-np.pi, np.pi, h_points):
            for psi in np.linspace(-np.pi / 2, np.pi / 2, v_points):
                w = np.array([[G * np.cos(psi) * np.cos(phi)], [G * np.sin(psi)], [G * np.cos(psi) * np.sin(phi)]])
                r = self.acc_to_raw(w)
                if self.__noise != 0:
                    r += np.random.normal(0, self.__noise, size=(3, 1))
                res.append(r)
        return res
    
    def acc_to_raw(self, w):
        return self.M @ self.F @ w + self.r0
    
    def raw_to_acc(self, r):
        return self.__iM @ r + self.__w0
    
    def update(self, params):
        self.M = np.diag([params[0], params[1], params[2]])
        self.F = np.array([
            [1, params[3], params[4]],
            [params[5], 1, params[6]],
            [params[7], params[8], 1]
        ])
        self.r0 = np.array([[params[9], params[10], params[11]]]).T
        self.__iM, self.__w0 = coefs_to_invert(self.M, self.F, self.r0)

    def update_inv(self, params):
        self.__iM = np.array([
            [params[0], params[3], params[4]],
            [params[5], params[1], params[6]],
            [params[7], params[8], params[2]]
        ])
        self.__w0 = np.array([[params[9], params[10], params[11]]]).T
        self.M, self.F, self.r0 = invert_to_coefs(self.__iM, self.__w0)
    
    def calibrate(self, func, raw_data, func_params):
        params = func(raw_data, func_params)
        self.update_inv(params)