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


def dim_scaling(dims, data_size, fn, data_dist, time_reps=100):
    print("Data dist: {} | fn: {}".format(data_dist, fn))  # , end="\r", flush=True)
    times = []
    # setup
    setup = ""
    setup += "import numpy as np;import infotheory;"
    setup += "dim={};"
    setup += "it = infotheory.InfoTools(dim, 1);"
    setup += "it.set_equal_interval_binning([100] * dim, [0] * dim, [1] * dim);"

    # varids
    if "mutual" in fn:
        setup += "varids = [0]*(int(dim/2)) + [1]*(dim - int(dim/2));"
    else:
        setup += (
            "varids = [0]*(int(dim/3)) + [1]*(int(dim/3)) + [2]*(dim - 2*int(dim/3));"
        )

    # distributions for data
    if data_dist == "uniform":
        setup += "data = np.random.rand({}, dim);".format(data_size)
    elif data_dist == "normal":
        setup += "data = np.random.normal(loc=0.5, scale=0.01, size=[{}, dim]);".format(
            data_size
        )

    setup += "it.add_data(data);"
    setup += "data = [];"

    # test time taken for each data size
    for dim in dims:
        print("\tTesting dim: {}".format(dim))
        setup = setup.format(dim)

        # functional call to information theoretic measure
        to_time = "it.{}(varids)".format(fn)

        # calling and measuing time taken over time_reps number of times
        t = timeit.timeit(to_time, setup=setup, number=time_reps)
        times.append(t / time_reps)

    return times


if __name__ == "__main__":
    dims = [3, 6, 10, 20, 50, 100]
    data_size = 10000

    plt.figure(figsize=[10, 3])
    for i, data_dist in enumerate(["normal", "uniform"]):
        plt.subplot(1, 2, i + 1)
        print("Scaling up mutual information")
        times = dim_scaling(dims, data_size, "mutual_info", data_dist)
        plt.plot(dims, times, marker="o", label="mutual_info")

        print("Scaling up unique information")
        times = dim_scaling(dims, data_size, "unique_info", data_dist)
        plt.plot(dims, times, marker="o", label="unique_info")

        print("Scaling up redundant information")
        times = dim_scaling(dims, data_size, "redundant_info", data_dist)
        plt.plot(dims, times, marker="o", label="redundant_info")

        print("Scaling up synergistic information")
        times = dim_scaling(dims, data_size, "synergy", data_dist)
        plt.plot(dims, times, marker="o", label="synergy")

        plt.xlabel("Data dimensionality")
        plt.ylabel("Execution Time (s)")
        plt.title("Data distribution: {}".format(data_dist))

    plt.legend(bbox_to_anchor=(1, 1.1))
    plt.tight_layout()
    plt.savefig("_dim_scaling.png")
    plt.show()
