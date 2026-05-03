# TM1
# Testing function, mode to critertia


import numpy as np
from scalar_algorithms import *
from utils.model import Imu
from utils.metrics import *
from utils.utils import *


# np.random.seed(45)


def testing(mode, calc_mode, debug=False, log_name='', conf_name='',
             modeling_params=None, func_params=None):
    imu0 = None
    raw_data = None

    if mode == 1:
        m_avg = modeling_params[0]
        w0_sig = modeling_params[2]
        phi_sig = modeling_params[1]
        noise = modeling_params[3]
        pos_count = 1
        if noise != 0:
            pos_count = 5  
        
        tM = np.abs(np.random.normal(m_avg, 0.2 * m_avg, size=(3, 1)))
        tphi = np.random.normal(0, phi_sig, size=(6, 1))
        tw0 = np.random.normal(w0_sig, w0_sig * 0.7, size=(3, 1))
        params = [tM[0, 0], tM[1, 0], tM[2, 0], tphi[0, 0], tphi[1, 0], tphi[2, 0], tphi[3, 0], tphi[4, 0], tphi[5, 0],
                  tw0[0, 0], tw0[1, 0], tw0[2, 0]]
        # print(params)
        imu0 = Imu(params, noise)
        # raw_data = imu0.generate_rotation()
        raw_data = imu0.generate_rotation_dodec(pos_count)
    elif mode == 2:
        params = imu_from_config(conf_name)
        imu0 = Imu(params)
        raw_data = log_reader(log_name)
    else:
        print('wrong mode')
        return
        
    imu1 = Imu()
    calibration_func = [nmnk, nmnk_draw]
    if calc_mode == 2:
        func_params.append(imu0)
    new_param, R_M, R_r0 = calibration_func[calc_mode - 1](raw_data, func_params)
    imu1.update_inv(new_param)

    
    tM = imu0.M
    tw0 = imu0.r0
    M = imu1.M
    w0 = imu1.r0
    tF = imu0.F
    F = imu1.F
    w1 = []
    w2 = []
    for r in raw_data:
        w1.append(imu0.raw_to_acc(r))
        w2.append(imu1.raw_to_acc(r))

    rel_err = [0] * 12
    for i in range(3):
        rel_err[i] = relative_error(M[i, i], tM[i, i])
        rel_err[i + 9] = relative_error(w0[i, 0], tw0[i, 0])
    rel_err[3] = relative_error(F[0, 2], tF[0, 2])
    rel_err[4] = relative_error(F[1, 0], tF[1, 0])
    rel_err[5] = relative_error(F[0, 1], tF[0, 1])
    rel_err[6] = relative_error(F[1, 2], tF[1, 2])
    rel_err[7] = relative_error(F[2, 0], tF[2, 0])
    rel_err[8] = relative_error(F[2, 1], tF[2, 1])

    abs_err = [0] * 12
    for i in range(3):
        abs_err[i] = absolute_error(M[i, i], tM[i, i])
        abs_err[i + 9] = absolute_error(w0[i, 0], tw0[i, 0])
    abs_err[3] = absolute_error(F[0, 2], tF[0, 2])
    abs_err[4] = absolute_error(F[1, 0], tF[1, 0])
    abs_err[5] = absolute_error(F[0, 1], tF[0, 1])
    abs_err[6] = absolute_error(F[1, 2], tF[1, 2])
    abs_err[7] = absolute_error(F[2, 0], tF[2, 0])
    abs_err[8] = absolute_error(F[2, 1], tF[2, 1])    
    
    if debug:
        print('--- Результат калибровки ---')

        print('R_M:')
        print(3 * np.sqrt(R_M))
        print('R_r0')
        print(3 * np.sqrt(R_r0))
        print('По осям:')
        axis = ['x', 'y', 'z']
        for i in range(3):
            print()
            print(f'Ось {axis[i]}')
            print(f'M true: {tM[i, i]:.5f}    {M[i, i]:.5f}    {relative_error(M[i, i], tM[i, i]):.2f}%    {absolute_error(M[i, i], tM[i, i]):.2f}')
            print(f'r0 true: {tw0[i, 0]:.2f}    {w0[i, 0]:.2f}    {relative_error(w0[i, 0], tw0[i, 0]):.2f}%     {absolute_error(w0[i, 0], tw0[i, 0]):.2f}')
        print()
        tM = imu0.F
        M = imu1.F
        print(f'Phi xz: {relative_error(M[0, 2], tM[0, 2]):.2f}%')
        print(f'Phi yx: {relative_error(M[1, 0], tM[1, 0]):.2f}%')
        print(f'Phi xy: {relative_error(M[0, 1], tM[0, 1]):.2f}%')
        print(f'Phi yz: {relative_error(M[1, 2], tM[1, 2]):.2f}%')
        print(f'Phi zx: {relative_error(M[2, 0], tM[2, 0]):.2f}%')
        print(f'Phi zy: {relative_error(M[2, 1], tM[2, 1]):.2f}%')
        print(average_accel_diff(w1, w2))
        print(avg_criteria(w2))

    return avg_criteria(w2), rel_err, abs_err