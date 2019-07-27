import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import infotheory

rnd = lambda x: np.round(x, decimals=4)


def get_pid_3D(data):
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # PID-ing
    u1 = it.unique_info([0, 1, 2])
    u2 = it.unique_info([0, 2, 1])
    r = it.redundant_info([0, 1, 2])
    s = it.synergy([0, 1, 2])
    return rnd(u1), rnd(u2), rnd(r), rnd(s)


def get_pid_4D(data):
    dims = np.shape(data)[1]
    it = infotheory.InfoTools(dims, 3)
    it.set_equal_interval_binning([10] * dims, np.min(data, 0), np.max(data, 0))
    it.add_data(data)
    # PID-ing
    u1 = it.unique_info([0, 1, 2, 3])
    u2 = it.unique_info([0, 2, 1, 3])
    u3 = it.unique_info([0, 2, 3, 1])
    r = it.redundant_info([0, 1, 2, 3])
    s = it.synergy([0, 1, 2, 3])
    return rnd(u1), rnd(u2), rnd(u3), rnd(r), rnd(s)


def plot_pid(subplot_ind, data, u1, u2, r, sy, title, u3=None):
    plt.subplot(subplot_ind)
    plt.scatter(
        np.linspace(0, 1, len(data[:, 0])),
        data[:, 0],
        label="T - Target",
        s=2,
        alpha=0.7,
    )
    plt.scatter(
        np.linspace(0, 1, len(data[:, 1])),
        data[:, 1],
        label="X - Source 1",
        s=2,
        alpha=0.7,
    )
    plt.scatter(
        np.linspace(0, 1, len(data[:, 2])),
        data[:, 2],
        label="Y - Source 2",
        s=2,
        alpha=0.7,
    )
    if np.shape(data)[1] == 4:
        plt.scatter(
            np.linspace(0, 1, len(data[:, 3])),
            data[:, 3],
            label="Z - Source 3",
            s=2,
            alpha=0.7,
        )
        title = title + "\n[u_x,u_y, u_z]={}\n[r,sy]={}".format([u1, u2, u3], [r, sy])
    else:
        title = title + "\n[u_x,u_y]={}\n[r,sy]={}".format([u1, u2], [r, sy])

    plt.title(title, fontsize=10)
    if str(subplot_ind)[-1] == "4":
        plt.legend(bbox_to_anchor=[1.1, 1.1])


plt.figure(figsize=[8, 6])
N = 500  # number of data points

## Case 1 - unq S
s = np.linspace(0, 1, N)
x = np.linspace(0, 1, N) + 0.1
y = np.zeros(N)
data = np.vstack([s.T, x.T, y.T]).T
u1, u2, r, sy = get_pid_3D(data)
plot_pid(221, data, u1, u2, r, sy, "3 var PID")

## Case 2 - unq A
s = np.linspace(0, 1, N)
x = np.zeros(N)
y = np.linspace(0, 1, N) + 0.1
data = np.vstack([s.T, x.T, y.T]).T
u1, u2, r, sy = get_pid_3D(data)
plot_pid(222, data, u1, u2, r, sy, "3 var PID")

## Case 3 - Redun S,A
s = np.linspace(0, 1, N)
x = np.linspace(0, 1, N) - 0.1
y = np.linspace(0, 1, N) + 0.1
data = np.vstack([s.T, x.T, y.T]).T
u1, u2, r, sy = get_pid_3D(data)
plot_pid(223, data, u1, u2, r, sy, "3 var PID")

## Case 4 - 4D PID
s = np.linspace(0, 1, N)
x = np.linspace(0, 1, N) - 0.1
y = (np.random.rand(N) - 0.1) * 1.1  # making the range same
z = (np.random.rand(N) - 0.1) * 1.1  # making the range same
data = np.vstack([s.T, x.T, y.T, z.T]).T
u1, u2, u3, r, sy = get_pid_4D(data)
plot_pid(224, data, u1, u2, r, sy, "4 var PID", u3)


plt.tight_layout()
plt.savefig("./pid_cont.png")
# plt.show()
