# TM1


import numpy as np
from scalar_algorithms import *
from turn_calibration import turn_calibration
from utils.model import Imu
from utils.metrics import *
from utils.utils import *


mode = int(input('Input mode:\n 1 - modeling,\n 2 - reading from log,\n 3 - turn clibration\nMode:'))

# np.random.seed(6447)
imu0 = None
raw_data = None

if mode == 1:
    m_sig = 0.0001
    w0_sig = 0.2
    mxx_sig = 0.01 * m_sig

    tMx = abs(np.random.normal(0, m_sig))
    tMy = abs(np.random.normal(0, m_sig))
    tMz = abs(np.random.normal(0, m_sig))
    tMxy = np.random.normal(0, mxx_sig)
    tMxz = np.random.normal(0, mxx_sig)
    tMyz = np.random.normal(0, mxx_sig)
    tw0 = np.random.normal(0, w0_sig, size=(3, 1))
    tM = np.array([
        [tMx, tMxy, tMxz],
        [tMxy, tMy, tMyz],
        [tMxz, tMxy, tMz]
    ])

    imu0 = Imu(tM, tw0)
    raw_data = imu0.generate_rotation()
elif mode == 2:
    raw_data = log_reader('logs/test.log')
    imu0 = imu_from_config('home_imu.conf')
    tM, tw0 = imu0.get_params()
elif mode == 3:
    raw_data = log_reader('logs/test.log')
    tM, tw0 = turn_calibration()
    imu0 = Imu(tM, tw0)
    save_imu_config(imu0, 'home_imu.conf')
else:
    print('Wrong code')
    exit()




# --- CALCULATION ---

M, w0 = mnk(raw_data)
imu1 = Imu(M, w0)

# --- CHECK ---
w1 = []
w2 = []
for r in raw_data:
    w1.append(imu0.raw_to_acc(r))
    w2.append(imu1.raw_to_acc(r))

print('--- Результат калибровки ---')
print('По осям:')
axis = ['x', 'y', 'z']
for i in range(3):
    print()
    print(f'Ось {axis[i]}')
    print(f'M true: {tM[i, i]:.2f}    {M[i, i]:.2f}    {relative_error(M[i, i], tM[i, i]):.2f}%')
    print(f'w0 true: {tw0[i, 0]:.2f}    {w0[i, 0]:.2f}    {relative_error(w0[i, 0], tw0[i, 0]):.2f}%')
print()
print(f'Mxy: {relative_error(M[0, 1], tM[0, 1]):.2f}%')
print(f'Mxz: {relative_error(M[0, 2], tM[0, 2]):.2f}%')
print(f'Myz: {relative_error(M[1, 2], tM[1, 2]):.2f}%')
print(average_absolute_accel_diff(w1, w2))
