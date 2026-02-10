# TM1
# Model of IMU sensor


import numpy as np


G = 9.81


class Imu():
    def __init__(self, M, w0, noise=0):
        self.__M = M
        self.__w0 = w0
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
        return np.linalg.inv(self.__M) @ (w - self.__w0)
    
    def raw_to_acc(self, r):
        return self.__M @ r + self.__w0
