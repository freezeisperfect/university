import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt
import statistics


def get_normalized_data_matrix(X):
    m = X.shape[0]
    A = (np.eye(m) - 1/m * np.ones((m, m))) @ X
    return A


def pca(X):
    A = get_normalized_data_matrix(X)
    w, v = np.linalg.eig(A.T @ A)

    desc_seq_ids = np.flip(np.argsort(w))
    w = w[desc_seq_ids]
    v = v[:, desc_seq_ids]

    w = np.sqrt(w)
    nu = 1/(X.shape[0] - 1)

    sigmas = []
    for num in w:
        sigmas.append(sqrt(nu) * num)
    sigmas = np.array(sigmas)

    return v.T, sigmas


def plot_power(s_d, name=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(1. + np.arange(len(s_d)), s_d, 'o--')
    ax.set_xlabel(r'$i$')
    ax.grid()
    if name is None:
        ax.set_ylabel(r'$\sqrt{\nu} \sigma_i$')
        plt.savefig('power_plot.png', dpi=750)
    else:
        ax.set_ylabel(r'$\sigma_i$')
        plt.savefig(f'{name}.png', dpi=750)
    plt.show()


def plot_data(A, principal_components, colors):
    fig, ax = plt.subplots(figsize=(8, 6))
    x_bar = [np.mean(A[:, 0]), np.mean(A[:, 1])]
    sigmas_bar = [statistics.stdev(A[:, 0]), statistics.stdev(A[:, 1])]
    A_bar = (A - x_bar) / sigmas_bar
    ax.scatter(A_bar[:, 0], A_bar[:, 1], c=colors, s=3)
    ax.plot([0], [0], 'ro', markersize=5)
    max_val = np.max(np.abs(A_bar))
    for pc in principal_components:
        ax.plot([0, max_val * pc[0]], [0, max_val * pc[1]], linewidth=3)
    ax.set_xlabel(r'$x_1$')
    ax.set_ylabel(r'$x_2$')
    ax.grid(alpha=0.6)
    plt.savefig('data_plot.png', dpi=750)
    plt.show()


if __name__ == "__main__":
    data = pd.read_csv('wdbc.data', header=None)
    id = data[0].values
    diagnosis = data[1].values
    target_data = {'id': id, 'diagnosis': diagnosis}
    target = pd.DataFrame(target_data)
    target['color'] = target['diagnosis'].apply(lambda x: (0.8, 0.3, 0.6) if x == 'B' else (0.2, 0.2, 1))

    data.pop(0)
    data.pop(1)
    data = data.values

    res_v, sigmas = pca(data)
    pr_comp = pd.DataFrame(res_v)
    pr_comp.to_excel('prcomp_result.xlsx', sheet_name='Sheet_1')
    plot_power(sigmas)

    res_v_test = res_v[:2]
    A = get_normalized_data_matrix(data)

    colors = target['color'].values
    plot_data(A @ res_v_test.T, res_v_test @ res_v_test.T, colors)
