import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

nv = 800
nt = 200
h = 0.5


if __name__ == "__main__":
    a_v = np.ones(800)
    a_v = a_v * 0.02

    b_v = np.ones(800)
    b_v = b_v * 0.2

    c_v = np.zeros(800)
    c_v = -65 + 15 * (np.random.default_rng().random(nv) ** 2)

    d_v = np.zeros(800)
    d_v = 8 - 6 * (np.random.default_rng().random(nv) ** 2)

    a_t = np.zeros(200)
    a_t = 0.02 + 0.08 * np.random.default_rng().random(nt)

    b_t = np.zeros(200)
    b_t = 0.25 - 0.05 * np.random.default_rng().random(nt)

    c_t = np.ones(200)
    c_t = c_t * (-65)

    d_t = np.ones(200)
    d_t = d_t * 2

    a = np.append(a_v, a_t)
    b = np.append(b_v, b_t)
    c = np.append(c_v, c_t)
    d = np.append(d_v, d_t)

    v = np.ones((1000)) * (-65.)
    u = b * v

    W1 = np.random.default_rng().random((1000, 800)) * 0.5

    W2 = np.random.default_rng().random((1000, 200)) * (-1)

    W = np.hstack((W1, W2))

    impulse = []

    t = np.arange(0, 1000, 1)
    for ti in t:
        f_matrix = v >= 30

        for i, is_impulse in enumerate(f_matrix):
            if is_impulse:
                impulse.append({'time': ti, 'id': i})

        v[f_matrix] = c[f_matrix]
        u[f_matrix] = u[f_matrix] + d[f_matrix]

        I = np.hstack((5 * np.random.default_rng().random(800), 2 * np.random.default_rng().random(200)))
        I = I + np.sum(W[:, f_matrix], axis=1)

        f1 = lambda v1, u1, I1: 0.04 * (v1 ** 2) + 5 * v1 + 140 - u1 + I1
        f2 = lambda v2, u2, a2, b2: a2 * (b2 * v2 - u2)

        i = 0

        while (i < int(1/h)):
            v_old = v
            u_old = u
            v = v_old + h * f1(v_old, u_old, I)
            u = u_old + h * f2(v_old, u_old, a, b)

            i += 1



    df = pd.DataFrame(impulse)

    exciting = df[df['id'] < 800]
    braking = df[df['id'] >= 800]
    plt.figure(figsize=(14, 9))
    plt.scatter(exciting['time'], exciting['id'], color='red', alpha=0.35)
    plt.scatter(braking['time'], braking['id'], color='blue', alpha=0.2)
    plt.savefig(f'neuron_activity.png', dpi=800)
    plt.show()