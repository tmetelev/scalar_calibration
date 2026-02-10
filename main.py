# TM1


import numpy as np
from model import Imu
from algorithm import *
from metrics import *


# np.random.seed(6447)

# Original parameters
m_sig = 50
w0_sig = 5
mxx_sig = 0.05

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

# tM = np.array([
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1]
# ])
# tw0 = np.array([[8, 0, 2]]).T


imu0 = Imu(tM, tw0)
raw_data = imu0.generate_rotation()

M, w0 = mnk(raw_data)
imu1 = Imu(M, w0)

# Check
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

