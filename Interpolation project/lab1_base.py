"""
Лабораторная работа №1. Базовая часть, продвинутая часть (задания 1, 2).
Пункты 3 и дальше выполнены в следующем модуле.
"""
import numpy as np
import matplotlib.pyplot as plt


def qubic_spline_coeff(x_nodes, y_nodes):
    main_matrix = np.zeros((int(len(x_nodes)), int(len(x_nodes))))
    result_matrix = np.zeros(len(x_nodes))
    result_matrix = result_matrix.T
    main_matrix[0, 0] = main_matrix[len(x_nodes) - 1, len(x_nodes) - 1] = 1
    counter = 0

    for i in range(1, len(x_nodes) - 1):
        main_matrix[i, counter] = h_n2 = x_nodes[i] - x_nodes[i-1]
        main_matrix[i, counter + 2] = h_n1 = x_nodes[i+1] - x_nodes[i]
        main_matrix[i, counter + 1] = 2 * (main_matrix[i, counter] + main_matrix[i, counter + 2])
        result_matrix[i] = (3 / h_n1) * (y_nodes[i+1] - y_nodes[i]) - (3 / h_n2) * (y_nodes[i] - y_nodes[i-1])
        counter += 1

    main_matrix_inv = np.linalg.inv(main_matrix)
    coeff_matrix = np.dot(main_matrix_inv, result_matrix)

    return coeff_matrix


def qubic_spline(x, qs_coeff, x_nodes, y_nodes):
    i = -1
    for n in range(0, len(x_nodes) - 1):
        if (x >= x_nodes[n]) and (x <= x_nodes[n+1]):
            i = n
            break
    if x < x_nodes[0]:
        i = 0
    if x > x_nodes[len(x_nodes) - 1]:
        i = len(x_nodes) - 2
    a_i = y_nodes[i]
    b_i = (1 / (x_nodes[i+1] - x_nodes[i])) * (y_nodes[i+1] - y_nodes[i]) - ((x_nodes[i+1] - x_nodes[i]) / 3) * (qs_coeff[i+1] + 2 * qs_coeff[i])
    c_i = qs_coeff[i]
    d_i = (qs_coeff[i+1] - qs_coeff[i]) / (3 * (x_nodes[i+1] - x_nodes[i]))
    S_x = a_i + b_i * (x - x_nodes[i]) + c_i * ((x - x_nodes[i]) ** 2) + d_i * ((x - x_nodes[i]) ** 3)

    return S_x


def d_qubic_spline(x, qs_coeff, x_nodes, y_nodes):
    for n in range(0, len(x_nodes)):
        if x >= x_nodes[n] and x <= x_nodes[n+1]:
            i = n
            break

    b_i = (1 / (x_nodes[i+1] - x_nodes[i])) * (y_nodes[i+1] - y_nodes[i]) - ((x_nodes[i+1] - x_nodes[i]) / 3) * (qs_coeff[i+1] + 2 * qs_coeff[i])
    c_i = qs_coeff[i]
    d_i = (qs_coeff[i+1] - qs_coeff[i]) / (3 * (x_nodes[i+1] - x_nodes[i]))
    S_dx = b_i + 2 * c_i * (x - x_nodes[i]) + 3 * d_i * ((x - x_nodes[i]) ** 2)

    return S_dx


# l_i - базисный полином
def l_i(i, x, x_nodes):
    l_x = 1

    for j in range(0, len(x_nodes)):
        if i == j:
            continue
        else:
            l_x = l_x * ((x - x_nodes[j]) / (x_nodes[i] - x_nodes[j]))

    return l_x


# L_i - значние полинома
def L(x, x_nodes, y_nodes):
    L_x = 0

    for i in range(0, len(x_nodes)):
        f_x_i = y_nodes[i]
        L_x = L_x + f_x_i * l_i(i, x, x_nodes)

    return L_x

if __name__ == "__main__":
    x_nodes = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    y_nodes = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]

    coeff = qubic_spline_coeff(x_nodes, y_nodes)

    x_q = np.array([])
    y_q = np.array([])
    interval = np.arange(x_nodes[0], x_nodes[len(x_nodes) - 1], 0.0005)
    print(interval)
    x_q = interval
    for node in interval:
        new_node = qubic_spline(node, coeff, x_nodes, y_nodes)
        y_q = np.append(y_q, new_node)

    plt.title('Апроксимация зависимости уровня поверхности жидкости h(x)')
    plt.grid(alpha=0.3)
    plt.plot(x_q, y_q, color='green')
    plt.scatter(x_nodes, y_nodes, color='red')
    plt.show()
