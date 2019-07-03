##############################################################################
# Infotheory demo to estimate MI over time between two 1D random vars
#
# Python demo
# Madhavun Candadai
# Jul 2019
##############################################################################
import infotheory
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


#######################################
## create data
#######################################
# system params
dt = 0.01
tau = 0.2

data = []
# creating stimuli of different amplitudes
for amp in np.arange(0.1, 1.1, 0.1):
    # stimulus signal given the amplitude
    stimulus = np.concatenate([np.zeros(100), amp * np.ones(100), np.zeros(100)])

    # resetting system for stimulus signal
    simple_integrator = 0.0
    t = 0.0
    trial_dat = []

    # providing stim to the system
    for stim in stimulus:
        simple_integrator += (dt / tau) * (-simple_integrator + stim)
        data.append([t, stim, simple_integrator])
        trial_dat.append(simple_integrator)
        t += dt

    plt.subplot(311)
    plt.plot(np.arange(0, t, dt), stimulus, "C0")
    plt.subplot(312)
    plt.plot(np.arange(0, t, dt), trial_dat, "C1")

data = np.array(data)

#######################################
## Analysis
#######################################
mi = []
# measuring informatino for each time point
for t in np.unique(data[:, 0]):
    # init object
    it = infotheory.InfoTools(2, 3)
    it.set_equal_interval_binning([10] * 2, [0] * 2, [1] * 2)

    # get data points for particular time and add them
    data_t = data[np.where(data[:, 0] == t)[0], 1:]
    it.add_data(data_t)

    # measure mutual information
    mi.append(it.mutual_info([0, 1]))

plt.subplot(313)
plt.plot(np.unique(data[:, 0]), mi, "C2")

plt.subplot(311)
plt.ylabel("Stimuli")
plt.subplot(312)
plt.ylabel("Recorded\ndata")
plt.subplot(313)
plt.ylabel("Mutual\ninformation")

plt.tight_layout()
plt.savefig("./mutual_info_t.png")
plt.show()
