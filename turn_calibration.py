# TM1
# Turn cailbration


import numpy as np
from utils.model import Imu
from utils.utils import save_imu_config
import serial
import time


text_arr = [
    'Z right, Y frwd',
    'Z right, Y back',
    'Z right, X back',
    'Z right, X frwd',
    'Y left, X back',
    'Y left, X frwd',
    'Y right, X back',
    'Z left, Y frwd',
    'Z left, X back'
]


def turn_calibration():
    pass
    ser = serial.Serial('/dev/ttyACM0', 9600)
    avg_raw = []
    # d X-Y
    for i in range(9):
        print(text_arr[i])
        input()
        ser.write(b'g\n')
        n = 0
        last_send_time = time.time()
        while True:
            if ser.in_waiting > 0:
                n = int(ser.readline().decode())
                break
            current_time = time.time()
            if current_time - last_send_time >= 5:
                print('Repeating request')
                ser.write(b'g\n')
                last_send_time = current_time
            time.sleep(0.1)
        raw = np.zeros((n, 3))
        print('Reading data')
        for j in range(n):
            raw[j] = np.array([[int(x) for x in ser.readline().decode().split()]])
        print('Done')
        avg_raw.append(np.average(raw.T, axis=1))

    g = 9.81

    Mx = (avg_raw[0][0] - avg_raw[1][0]) / (2 * g)
    My = (avg_raw[2][1] - avg_raw[3][1]) / (2 * g)
    Mz = (avg_raw[4][2] - avg_raw[5][2]) / (2 * g)

    phi_xy = (avg_raw[2][0] - avg_raw[3][0]) / (2 * g)
    phi_xz = (avg_raw[4][0] - avg_raw[5][0]) / (2 * g)
    phi_yx = (avg_raw[0][1] - avg_raw[1][1]) / (2 * g)
    phi_yz = (avg_raw[4][1] - avg_raw[6][1]) / (2 * g)
    phi_zx = (avg_raw[0][2] - avg_raw[7][2]) / (2 * g)
    phi_zy = (avg_raw[2][2] - avg_raw[8][2]) / (2 * g)

    rx0 = (avg_raw[0][0] + avg_raw[1][0]) / (2)
    ry0 = (avg_raw[2][1] + avg_raw[3][1]) / (2)
    rz0 = (avg_raw[4][2] + avg_raw[5][2]) / (2)
    return [Mx, My, Mz, phi_xy, phi_xz, phi_yx, phi_yz, phi_zx, phi_zy, rx0, ry0, rz0] 

params = turn_calibration()
imu0 = Imu(params)
save_imu_config(params, 'home_imu.conf')