# TM1
# Metrics 


def average_accel_diff(w1, w2):
    n = len(w1)
    res = 0
    for i in range(n):
        res += abs(w1[i].T @ w1[i] - w2[i].T @ w2[i])
    res /= (n * 9.81 * 9.81)
    return res

def relative_error(x, x0):
    return abs((x - x0) / x0) * 100

def avg_criteria(w):
    n = len(w)
    res = 0
    for i in range(n):
        res += w[i].T @ w[i] - 9.81 * 9.81
    res /= (n)
    return res
