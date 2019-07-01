import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import infotheory

rnd = lambda x: np.round(x, decimals=4)


def get_pid(data):
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 1)
    it.set_equal_interval_binning([50] * dims, [0] * dims, [1] * dims)
    it.add_data(data)
    mi = it.mutual_info([0, 1, 1])
    u1 = it.unique_info([0, 1, 2])
    u2 = it.unique_info([0, 2, 1])
    r = it.redundant_info([0, 1, 2])
    s = it.synergy([0, 1, 2])
    return rnd(mi), rnd(u1), rnd(u2), rnd(r), rnd(s)


def plot_pid(subplot_ind, data, mi, u1, u2, r, sy):
    plt.subplot(subplot_ind)
    plt.scatter(
        np.linspace(0, 1, len(data[:, 0])), data[:, 0], label="S", s=2, alpha=0.7
    )
    plt.scatter(
        np.linspace(0, 1, len(data[:, 1])), data[:, 1], label="X", s=2, alpha=0.7
    )
    plt.scatter(
        np.linspace(0, 1, len(data[:, 2])), data[:, 2], label="Y", s=2, alpha=0.7
    )
    plt.title(
        "mi={}\n[u_x,u_y]={}\n[r,sy]={}".format(mi, [u1, u2], [r, sy]), fontsize=10
    )
    if str(subplot_ind)[-1] == "1":
        plt.legend()


plt.figure(figsize=[6, 6])

## Case 1 - unq S
s = np.linspace(0, 1, 200)
x = np.linspace(0, 1, 200) + 0.1
y = np.zeros(200)
data = np.vstack([s.T, x.T, y.T]).T
mi, u1, u2, r, sy = get_pid(data)
plot_pid(221, data, mi, u1, u2, r, sy)

## Case 2 - unq A
s = np.linspace(0, 1, 200)
x = np.zeros(200)
y = np.linspace(0, 1, 200) + 0.1
data = np.vstack([s.T, x.T, y.T]).T
mi, u1, u2, r, sy = get_pid(data)
plot_pid(222, data, mi, u1, u2, r, sy)

## Case 3 - Redun S,A
s = np.linspace(0, 1, 200)
x = np.linspace(0, 1, 200) - 0.1
y = np.linspace(0, 1, 200) + 0.1
data = np.vstack([s.T, x.T, y.T]).T
mi, u1, u2, r, sy = get_pid(data)
plot_pid(223, data, mi, u1, u2, r, sy)

## Case 4 - Syn S,A
s = np.linspace(0, 1, 200)
x = np.linspace(0, 1, 200)
y = 1 - np.linspace(0, 1, 200)
s[100:] = 1 - s[100:]
s += 0.1
data = np.vstack([s.T, x.T, y.T]).T
mi, u1, u2, r, sy = get_pid(data)
plot_pid(224, data, mi, u1, u2, r, sy)

plt.tight_layout()
# plt.savefig("./test_pid_sanity.png")
plt.show()
