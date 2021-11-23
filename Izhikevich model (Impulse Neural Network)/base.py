import matplotlib.pyplot as plt
from scipy.optimize import root, fsolve
import numpy as np
import time

I = 5
t0 = 0
tn = 300
h = 0.1


def condition_check(w, coeff):
    if w[0] >= 30:
        w[0] = coeff['c']
        w[1] = w[1] + coeff['d']
    return w


def derivative(func, w, t):
    dvdt = func[0](w)
    dudt = func[1](w)
    result = np.array([dvdt, dudt])
    return result


def euler(x_0, t_0, t_n, f, h, coeff):
    start_t = time.time()
    t = np.arange(t_0, t_n, h)

    row = int(len(t))
    col = int(len(x_0))

    w = np.zeros((row, col))
    w[0] = x_0
    w[0] = condition_check(w[0], coeff)
    print(w.shape)
    i = 0
    for ti in t[:-1]:
        result = w[i] + h * derivative(f, w[i], ti)
        w[i + 1] = result
        w[i + 1] = condition_check(w[i + 1], coeff)
        i += 1

    return w, start_t


def implicit_euler(x_0, t_0, t_n, f, h, coeff):
    start_t = time.time()
    t = np.arange(t_0, t_n, h)

    row = int(len(t))
    col = int(len(x_0))

    w = np.zeros((row, col))
    w[0] = x_0
    w[0] = condition_check(w[0], coeff)

    i = 0
    for ti in t[:-1]:
        f_t = lambda w1: w1 - h * derivative(f, w1, ti) - w[i]
        sol = root(f_t, w[i])
        w[i + 1] = sol.x
        w[i + 1] = condition_check(w[i + 1], coeff)
        i += 1

    return w, start_t


def runge_kutta(x_0, t_0, t_n, f, h, coeff):
    start_t = time.time()
    t = np.arange(t_0, t_n, h)

    row = int(len(t))
    col = int(len(x_0))

    w = np.zeros((row, col))
    w[0] = x_0
    w[0] = condition_check(w[0], coeff)

    k1 = lambda w, ti: h * derivative(f, w, ti)
    k2 = lambda w, ti: h * derivative(f, w + 0.5 * k1(w, ti), ti + h/2)
    k3 = lambda w, ti: h * derivative(f, w + 0.5 * k2(w, ti), ti + h/2)
    k4 = lambda w, ti: h * derivative(f, w + k3(w, ti), ti + h)

    i = 0
    for ti in range(len(t) - 1):
        w[i + 1] = w[i] + (1/6) * (k1(w[i], ti) + 2 * k2(w[i], ti) + 2 * k3(w[i], ti) + k4(w[i], ti))
        w[i + 1] = condition_check(w[i + 1], coeff)
        i += 1

    return w, start_t


# w[0] = v, w[1] = u
if __name__ == "__main__":
    table = [
        {'name': 'Tonic Spiking', 'a': 0.02, 'b': 0.2, 'c': -65, 'd': 6},
        {'name': 'Phasic Spiking', 'a': 0.02, 'b': 0.25, 'c': -65, 'd': 6},
        {'name': 'Chattering', 'a': 0.02, 'b': 0.2, 'c': -50, 'd': 2},
        {'name': 'Fast Spiking', 'a': 0.1, 'b': 0.2, 'c': -65, 'd': 2}
    ]
    t = np.arange(t0, tn, h)
    for item in table:
        a = item['a']
        b = item['b']
        dvdt = lambda w: 0.04 * (w[0] ** 2) + 5 * w[0] + 140 - w[1] + I
        dudt = lambda w: a * (b * w[0] - w[1])

        func = [dvdt, dudt]
        start_conditions = np.array([item['c'], item['c'] * item['b']])
        w1, t1 = euler(start_conditions, t0, tn, func, h, item)
        tk1 = time.time()
        w2, t2 = implicit_euler(start_conditions, t0, tn, func, h, item)
        tk2 = time.time()
        w3, t3 = runge_kutta(start_conditions, t0, tn, func, h, item)
        tk3 = time.time()
        print('euler:', tk1-t1, 'imp euler:', tk2-t2, 'runge-kutta:', tk3-t3)

        plt.figure(figsize=(14, 9))
        plt.title(item['name'])
        plt.grid(alpha=0.6)
        plt.plot(t, w1.T[0], marker='o', color='red', label='euler', alpha=0.6, markersize=5, linewidth=0.5)
        plt.plot(t, w2.T[0], marker='o', color='green', label='backward euler', alpha=0.3, markersize=5, linewidth=0.5)
        plt.plot(t, w3.T[0], marker='o', color='purple', label='runge-kutta', alpha=0.6, markersize=5, linewidth=0.5)
        plt.legend()
        name = item['name']

        # plt.savefig(f'{name}.png', dpi=800)
        # plt.show()
