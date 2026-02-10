# TM1


import numpy as np
from model import Imu


np.random.seed(42)

# Original parameters
m_sig = 10
w0_sig = 2
mxx_sig = 0.05

tMx = np.random.normal(0, m_sig)
tMy = np.random.normal(0, m_sig)
tMz = np.random.normal(0, m_sig)
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
raw_data = imu0.generate_rotation(2, 3)
