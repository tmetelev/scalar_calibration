# TM1


from testing import testing


# mode = int(input('Input imu mode:\n 1 - modeling,\n 2 - reading from config\nMode:'))
# print()
# calc_mode = int(input("Calculation mode:\n 1 - NMNK\nMode:"))
# print('\n\n')
# testing(mode, calc_mode, debug=True, modeling_params=[2000, 1e-2, 100])
testing(1, 1, debug=True, modeling_params=[2000, 0.1, 500, 0], func_params=[100])
# testing(1, 2, debug=True, modeling_params=[2000, 0.1, 500, 50], func_params=[25, 0])