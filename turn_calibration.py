# TM1
# Turn cailbration


import numpy as np
from utils.model import Imu
from utils.utils import save_imu_config
# import serial
import time


text_arr = [
    'Put X axis down, press ENTER when ready',
    'Rotate around Z axis, press ENTER when ready',
    'Put Y axis down, press ENTER when ready',
    'Rotate around Z axis, press ENTER when ready',
    'Put Z axis down, press ENTER when ready',
    'Rotate around Y axis, press ENTER when ready',
    'Return to previous pose. Rotate around X axis, press ENTER when ready'
]


def turn_calibration():
    pass
    # ser = serial.Serial('/dev/ttyACM0', 9600)
    # avg_raw = []
    # # d X-Y
    # for i in range(7):
    #     print(text_arr[i])
    #     input()
    #     ser.write(b'g\n')
    #     n = 0
    #     last_send_time = time.time()
    #     while True:
    #         if ser.in_waiting > 0:
    #             n = int(ser.readline().decode())
    #             break
    #         current_time = time.time()
    #         if current_time - last_send_time >= 5:
    #             print('Repeating request')
    #             ser.write(b'g\n')
    #             last_send_time = current_time
    #         time.sleep(0.1)
    #     raw = np.zeros((n, 3))
    #     print('Reading data')
    #     for j in range(n):
    #         raw[j] = np.array([[int(x) for x in ser.readline().decode().split()]])
    #     print('Done')
    #     avg_raw.append(np.average(raw.T, axis=1))
    # Mx = avg_raw[0][0] - avg_raw[1][0]
    # My = avg_raw[2][1] - avg_raw[3][1]
    # Mz = avg_raw[4][2] - avg_raw[5][2]
    # Mxy = avg_raw[2][0] - avg_raw[3][0]
    # Mxz = avg_raw[4][0] - avg_raw[5][0]
    # Myz = avg_raw[4][1] - avg_raw[6][1]
    # wx0 = avg_raw[0][0] + avg_raw[1][0]
    # wy0 = avg_raw[2][1] + avg_raw[3][1]
    # wz0 = avg_raw[4][2] + avg_raw[5][2]
    # Ms = np.array([
    #     [Mx, Mxy, Mxz],
    #     [-Mxy, My, Myz],
    #     [-Mxz, -Myz, Mz]
    # ])
    # Ms /= 2 * 9.81
    # w0s = np.array([[wx0, wy0, wz0]]).T
    # w0s /= 2
    # M = np.linalg.inv(Ms)
    # w0 = -M @ w0s
    # return M, w0

# tM, tw0 = turn_calibration()
# imu0 = Imu(tM, tw0)
# save_imu_config(imu0, 'home_imu.conf')