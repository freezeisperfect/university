"""
Лабораторная работа №1. Продвинутая часть (задания 3, 4, 5).
Пункты 3 и дальше выполнены в этом файле. Функции из предыдущих пунктов импортированы.
"""

from lab1_base import qubic_spline_coeff, qubic_spline, d_qubic_spline, l_i, L
import numpy as np
import matplotlib.pyplot as plt
import statistics


# 3 (a)
# x_nodes - изначальный вектор, scale - стандартное отклонение, n - количество векторов
def generate_vectors(vector, scale, n):
    res = []

    for i in range(0, n):

        res_iteration = []
        for j in range(0, len(vector)):
            Z = np.random.normal(0, scale)
            new_elem = vector[j] + Z
            res_iteration.append(new_elem)
        res.append(res_iteration)
    result = np.array(res)

    return result


# 3 (b)
def make_interpolants_x(x_nodes_res, x_nodes, y_nodes):
    for n in range(len(x_nodes_res)):
        res_iterate = []

        interval = np.arange(0.00, 1.0001, 0.005)
        interval_list = interval.tolist()
        for m in interval:
            value = L(m, x_nodes_res[n], y_nodes)
            res_iterate.append(value)

        plt.plot(interval_list, res_iterate)

    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Интерполяция методом Лагранжа с измененными x_nodes')
    plt.grid(alpha=0.4)
    plt.show()




# 3 (c, d)
def make_trust_interval_x(x_nodes, y_nodes, x_nodes_res):
    interval_x = np.arange(0.00, 1.0001, 0.005)

    h_l = []
    h_u = []
    median = []

    for x in interval_x:
        temp = []
        for i in range(len(x_nodes_res)):
            f = L(x, x_nodes_res[i], y_nodes)
            temp.append(f)
        temp = sorted(temp)
        h_l.append(temp[49])
        h_u.append(temp[948])
        median.append(statistics.median(temp))

    plt.plot(interval_x, h_l, color='green', label='h_l(x)')
    plt.plot(interval_x, h_u, color='orange', label='h_u(x)')
    plt.plot(interval_x, median, color='blue', label='median')
    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Графики h_l(x), h_u(x), усредненный интерполянт')
    plt.grid()
    plt.legend()
    plt.show()


# 4 (b)
def make_interpolants_y(y_nodes_res, x_nodes, y_nodes):
    for n in range(len(y_nodes_res)):
        res_iterate = []
        interval = np.arange(0.00, 1.0001, 0.005)
        interval_list = interval.tolist()

        for m in interval:
            value = L(m, x_nodes, y_nodes_res[n])
            res_iterate.append(value)

        plt.plot(interval_list, res_iterate)

    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Интерполяция методом Лагранжа с измененными y_nodes')
    plt.grid()
    plt.show()


def make_trust_interval_y(x_nodes, y_nodes, y_nodes_res):
    interval_x = np.arange(0.00, 1.0001, 0.005)

    h_l = []
    h_u = []
    median = []

    for x in interval_x:
        temp = []
        for i in range(len(y_nodes_res)):
            f = L(x, x_nodes, y_nodes_res[i])
            temp.append(f)
        temp = sorted(temp)
        h_l.append(temp[48])
        h_u.append(temp[947])
        median.append(statistics.median(temp))

    plt.plot(interval_x, h_l, color='green', label='h_l(x)')
    plt.plot(interval_x, h_u, color='orange', label='h_u(x)')
    plt.plot(interval_x, median, color='blue', label='median', linewidth='1')
    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Графики h_l(x), h_u(x), усредненный интерполянт')
    plt.grid()
    plt.legend()
    plt.show()


# 5 (1st)
def make_qubic_splines_x(x_nodes, y_nodes, x_nodes_res):
    for n in range(len(x_nodes_res)):
        c = qubic_spline_coeff(x_nodes_res[n], y_nodes)
        interval_x = np.arange(0.00, 1.0001, 0.005)
        res_iterate = []

        for x in interval_x:
            S = qubic_spline(x, c, x_nodes_res[n], y_nodes)
            res_iterate.append(S)

        interval_y = np.array(res_iterate)
        plt.plot(interval_x, interval_y)

    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Интерполяция кубическими сплайнами с измененными x_nodes')
    plt.grid()
    plt.show()


def make_trust_interval_qubic_x(x_nodes, y_nodes, x_nodes_res):
    interval_x = np.arange(0.00, 1.0001, 0.01)

    h_l = []
    h_u = []
    median = []

    for x in interval_x:
        temp = []
        for n in range(len(x_nodes_res)):
            x_nodes_i = x_nodes_res[n]
            c = qubic_spline_coeff(x_nodes_i, y_nodes)
            S = qubic_spline(x, c, x_nodes_i, y_nodes)
            temp.append(S)

        temp = sorted(temp)
        h_l.append(temp[48])
        h_u.append(temp[947])
        median.append(statistics.median(temp))

    plt.plot(interval_x, h_l, color='green', label='h_l(x)')
    plt.plot(interval_x, h_u, color='orange', label='h_u(x)')
    plt.plot(interval_x, median, color='blue', label='median', linewidth='1')
    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Графики h_l(x), h_u(x), усредненный интерполянт, интерполяция кубическими \n' + 'сплайнами с использованием x_tilde')
    plt.grid()
    plt.legend()
    plt.show()


# 5 (2nd)
def make_qubic_splines_y(x_nodes, y_nodes, y_nodes_res):
    for n in range(len(y_nodes_res)):
        c = qubic_spline_coeff(x_nodes, y_nodes_res[n])
        interval_x = np.arange(x_nodes[0], x_nodes[len(x_nodes) - 1], 0.0005)
        res_iterate = []

        for x in interval_x:
            y_nodes_i = y_nodes_res[n]
            S = qubic_spline(x, c, x_nodes, y_nodes_i)
            res_iterate.append(S)

        interval_y = np.array(res_iterate)
        plt.plot(interval_x, interval_y)

    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Интерполяция кубическими сплайнами с измененными y_nodes')
    plt.grid()
    plt.show()


def make_trust_interval_qubic_y(x_nodes, y_nodes, y_nodes_res):
    interval_x = np.arange(0.00, 1.0001, 0.01)

    h_l = []
    h_u = []
    median = []

    for x in interval_x:
        temp = []
        for n in range(len(y_nodes_res)):
            y_nodes_i = y_nodes_res[n]
            c = qubic_spline_coeff(x_nodes, y_nodes_i)
            S = qubic_spline(x, c, x_nodes, y_nodes_i)
            temp.append(S)

        temp = sorted(temp)
        h_l.append(temp[48])
        h_u.append(temp[947])
        median.append(statistics.median(temp))

    plt.plot(interval_x, h_l, color='green', label='h_l(x)')
    plt.plot(interval_x, h_u, color='orange', label='h_u(x)')
    plt.plot(interval_x, median, color='blue', label='median', linewidth='1')
    plt.scatter(x_nodes, y_nodes, color='red')
    plt.title('Графики h_l(x), h_u(x), усредненный интерполянт, интерполяция кубическими \n' + 'сплайнами с использованием y_tilde')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    x_nodes = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    y_nodes = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]

    # 3a
    x_tilde = generate_vectors(x_nodes, 10 ** (-2), 1000)

    # 3b (uncomment)
    # make_interpolants_x(x_tilde, x_nodes, y_nodes)

    # 3cd (uncomment)
    # make_trust_interval_x(x_nodes, y_nodes, x_tilde)

    # 4a (uncomment)
    # y_tilde = generate_vectors(y_nodes, 10 ** (-2), 1000)

    # 4b (uncomment)
    # make_interpolants_y(y_tilde, x_nodes, y_nodes)

    # 4cd (uncomment)
    # make_trust_interval_y(x_nodes, y_nodes, y_tilde)

    # 5 (uncomment)
    # make_qubic_splines_x(x_nodes, y_nodes, x_tilde)

    # make_trust_interval_qubic_x(x_nodes, y_nodes, x_tilde)

    # make_qubic_splines_y(x_nodes, y_nodes, y_tilde)

    # make_trust_interval_qubic_y(x_nodes, y_nodes, y_tilde)