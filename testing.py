# TM1
# Testing function, mode to critertia


import numpy as np
from scalar_algorithms import *
from turn_calibration import turn_calibration
from utils.model import Imu
from utils.metrics import *
from utils.utils import *


def testing(mode, calc_mode, debug=False, log_name=None, conf_name=None,
             modeling_params=None, kalman_params=None):
    imu0 = None
    raw_data = None

    if mode == 1:
        m_sig = modeling_params[0]
        w0_sig = modeling_params[1]
        phi_sig = modeling_params[2]
        
        tM = np.random.normal(0, m_sig, size=(3, 1))
        tphi = np.random.normal(0, phi_sig, size=(6, 1))
        tw0 = np.random.normal(0, w0_sig, size=(3, 1))
        params = [tM[0], tM[1], tM[2], tphi[0], tphi[1], tphi[2], tphi[3], tphi[4], tphi[5],
                  tw0[0], tw0[1], tw0[2]]
        imu0 = Imu(params)
    elif mode == 2:
        imu0 = imu_from_config(conf_name)
    
    # TODO: Доделать тестирование, исправить алгоритм НМНК, пересчитать математику
    if calc_mode == 1:
        




    # --- CALCULATION ---
    calc_mode = int(input("Calculation mode:\n 1 - MNK\n 2 - N_MNK\n 3 - Kalman\nMode:"))
    print('\n\n')
    if calc_mode == 1:
        M, w0 = mnk(raw_data)
    elif calc_mode == 2:
        M, w0 = nmnk(raw_data, 100)
    elif calc_mode == 3:
        if mode == 1:
            sig_x = m_sig ** 2
            sig_xx = mxx_sig ** 2
            sig_w0 = w0_sig ** 2
        else:
            sig_x = 1e-4 ** 2
            sig_xx = 1e-7 ** 2
            sig_w0 = 1 ** 2
        M, w0 = kalman(raw_data, np.array([[800 ** 2]]), np.diag([sig_x, sig_x, sig_x, sig_xx, sig_xx, sig_xx,
                                                sig_w0, sig_w0, sig_w0]))
    else:
        print('Wrong code')
        exit()

    imu1 = Imu(M, w0)
    imu0 = Imu(tM, tw0)
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
        print(f'M true: {tM[i, i]:.5f}    {M[i, i]:.5f}    {relative_error(M[i, i], tM[i, i]):.2f}%')
        print(f'w0 true: {tw0[i, 0]:.2f}    {w0[i, 0]:.2f}    {relative_error(w0[i, 0], tw0[i, 0]):.2f}%')
    print()
    print(f'Mxy: {relative_error(M[0, 1], tM[0, 1]):.2f}%')
    print(f'Mxz: {relative_error(M[0, 2], tM[0, 2]):.2f}%')
    print(f'Myz: {relative_error(M[1, 2], tM[1, 2]):.2f}%')
    print(average_accel_diff(w1, w2))
    print(avg_criteria(w2))