# TM1
# Metrics 


def average_absolute_accel_diff(w1, w2):
    n = len(w1)
    res = 0
    for i in range(n):
        res += (w1[i].T @ w1[i] - w2[i].T @ w2[i]) ** 2
    res /= n
    return res

def relative_error(x, x0):
    return abs((x - x0) / x0) * 100
