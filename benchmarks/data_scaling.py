###############################################################################
# Scalability benchmark
#
# Madhavun Candadai
# Dec, 2018
#
# Plotting time taken as dimensionality increases
###############################################################################
import os
import timeit
import numpy as np

import infotheory

import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def data_scaling(data_sizes, dim, fn, data_dist, time_reps=100):
    print("Data dist: {} | fn: {}".format(data_dist, fn))  # , end="\r", flush=True)
    times = []

    # setup
    setup = ""
    setup += "import numpy as np;import infotheory;"
    setup += "dim={};".format(dim)
    setup += "it = infotheory.InfoTools(dim, 1);"
    setup += "it.set_equal_interval_binning([100] * dim, [0] * dim, [1] * dim);"

    # varids
    if dim == 2:
        setup += "varids = [0,1];"
    elif dim == 3:
        setup += "varids = [0,1,2];"

    # distributions for data
    if data_dist == "uniform":
        setup += "data = np.random.rand({}, dim);"
    elif data_dist == "normal":
        setup += "data = np.random.normal(loc=0.5, scale=0.01, size=[{}, dim]);"

    setup += "it.add_data(data);"
    setup += "data = [];"

    # test time taken for each data size
    for data_size in data_sizes:
        print("\tTesting data size of {}".format(data_size))
        setup = setup.format(data_size)

        # functional call to information theoretic measure
        to_time = "it.{}(varids)".format(fn)

        # calling and measuing time taken over time_reps number of times
        t = timeit.timeit(to_time, setup=setup, number=time_reps)
        times.append(t / time_reps)

    return times


if __name__ == "__main__":
    data_sizes = [1000, 10000, 20000, 40000, 60000, 80000, 100000]

    plt.figure(figsize=[10, 3])
    for i, data_dist in enumerate(["normal", "uniform"]):
        plt.subplot(1, 2, i + 1)
        print("Scaling up mutual information")
        times = data_scaling(data_sizes, 2, "mutual_info", data_dist)
        plt.plot(data_sizes, times, marker="o", label="mutual_info")

        print("Scaling up unique information")
        times = data_scaling(data_sizes, 3, "unique_info", data_dist)
        plt.plot(data_sizes, times, marker="o", label="unique_info")

        print("Scaling up redundant information")
        times = data_scaling(data_sizes, 3, "redundant_info", data_dist)
        plt.plot(data_sizes, times, marker="o", label="redundant_info")

        print("Scaling up synergistic information")
        times = data_scaling(data_sizes, 3, "synergy", data_dist)
        plt.plot(data_sizes, times, marker="o", label="synergy")

        plt.xlabel("Num data points")
        plt.ylabel("Execution Time (s)")
        plt.xscale("log")
        plt.title("Data distribution: {}".format(data_dist))

    plt.legend(bbox_to_anchor=(1, 1.1))
    plt.tight_layout()
    plt.savefig("data_scaling.png")
    plt.show()
