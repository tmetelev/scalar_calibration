# TM1


from testing import testing


# mode = int(input('Input imu mode:\n 1 - modeling,\n 2 - reading from config\nMode:'))
# print()
# calc_mode = int(input("Calculation mode:\n 1 - NMNK\nMode:"))
# print('\n\n')
# testing(mode, calc_mode, debug=True, modeling_params=[2000, 1e-2, 100])
testing(1, 1, debug=True, modeling_params=[2000, 0.01, 500, 50], func_params=[20, 50])

# testing(2, 1, debug=True, modeling_params=[2000, 0.01, 500, 10], func_params=[20, 100], conf_name='home_imu.conf', log_name='logs/long.log')


# testing(1, 2, debug=True, modeling_params=[2000, 0.1, 500, 50], func_params=[20, 0])