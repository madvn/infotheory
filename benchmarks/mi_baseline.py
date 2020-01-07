###############################################################################
# Mutual Information baseline
#
# Madhavun Candadai
# Dec, 2018
#
# Mutual information should be high for identical variables, slightly lower for
# noisy identical variables and low for random variables
###############################################################################
import infotheory
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def sub_plt(ind, data, mi):
    plt.subplot(ind)
    plt.plot(data[0], data[1], ".", markersize=2)
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel("Random variable, X", fontsize=12)
    plt.ylabel("Random variable, Y", fontsize=12)
    plt.title("Mutual information\n {}".format(np.round(mi, 4)), fontsize=13)


plt.figure(figsize=[10, 3])

# identical variables
x = np.arange(0, 1, 1 / 1000)
y = np.flipud(x)
it = infotheory.InfoTools(2, 0)
it.set_equal_interval_binning([50] * 2, [0] * 2, [1] * 2)
it.add_data(np.vstack([x, y]).T)
mi = it.mutual_info([0, 1]) / np.log2(50)
sub_plt(141, [x, y], mi)

# shuffled identical variables
inds = np.arange(0.05, 1, 0.1)
x = [np.random.normal(loc=id, scale=0.015, size=[30]) for id in inds]
x = np.asarray(x).flatten()
s_inds = np.random.permutation(inds)
y = [np.random.normal(loc=id, scale=0.015, size=[30]) for id in s_inds]
y = np.asarray(y).flatten()
it = infotheory.InfoTools(2, 0)
it.set_equal_interval_binning([10] * 2, [0] * 2, [1] * 2)
it.add_data(np.vstack([x, y]).T)
mi = it.mutual_info([0, 1]) / np.log2(10)
sub_plt(142, [x, y], mi)

# noisy identical variables
x = np.random.rand(1000)
y = x + (np.random.randn(1000) * 0.02)
it = infotheory.InfoTools(2, 3)
it.set_equal_interval_binning([50] * 2, [np.min(x), np.min(y)], [np.max(x), np.max(y)])
it.add_data(np.vstack([x, y]).T)
mi = it.mutual_info([0, 1]) / np.log2(50)
sub_plt(143, [x, y], mi)

# random variables
x = np.random.rand(1000)
y = np.random.rand(1000)
it = infotheory.InfoTools(2, 3)
it.set_equal_interval_binning([50] * 2, [np.min(x), np.min(y)], [np.max(x), np.max(y)])
it.add_data(np.vstack([x, y]).T)
mi = it.mutual_info([0, 1]) / np.log2(50)
sub_plt(144, [x, y], mi)

plt.tight_layout()
plt.savefig("mi_baseline.png")
plt.show()
