###############################################################################
# Scalability benchmark
#
# Madhavun Candadai
# Dec, 2018
#
# Plotting time taken as dimensionality increases
###############################################################################
import os
import time
import numpy as np
import infotheory
import matplotlib.pyplot as plt

def scalibility(fn, dims, time_reps, num_datapoints, data_dist):
    times = []
    for dim in dims:
        print('\tDimensionality of {}'.format(dim))
        sdim = str(dim)
        it = infotheory.InfoTools(dim,1,[100]*dim,[0]*dim,[1]*dim)
        # setting up appropriate var_IDs for each case
        if 'entropy' in fn:
            varids = np.ones(dim);
        elif ('redun' in fn) or ('synergy' in fn) or ('unique' in fn):
            varids = np.random.randint(3,size=[dim])
        else:
            varids = np.random.randint(2,size=[dim])

        # distributions for data
        if data_dist == "uniform":
            data = np.random.rand(num_datapoints,dim)
        elif data_dist == "normal":
            data = np.random.normal(loc=0.5,scale=0.1,size=[num_datapoints,dim])
        it.add_data(data)
        data = []

        # functional call to information theoretic measure
        if fn == 'entropy':
            t_before = time.time()
            for _ in range(time_reps):
                it.entropy(varids)
            t_after = time.time()
        elif fn == 'mutual_info':
            t_before = time.time()
            for _ in range(time_reps):
                it.mutual_info(varids)
            t_after = time.time()
        elif fn == 'synergy':
            t_before = time.time()
            for _ in range(time_reps):
                it.synergy(varids)
            t_after = time.time()
        times.append(t_after-t_before)

    return np.asarray(times)/time_reps # average

if __name__ == "__main__":
    for data_dist in ['uniform', 'normal']:
        # config for timing
        time_reps = 1000 # number of runs to average over
        dims = 2**np.asarray([2,5,8,9,10])
        num_datapoints = 10000
        fns = ['mutual_info','entropy','synergy']
        plt.figure(figsize=[4,3])

        print("Functions to check: {}".format(fns))
        # for each info theoretic measure
        for fn in fns:
            print("Running for {}".format(fn))
            filename = fn+'_timeReps{}_{}.npy'.format(time_reps,data_dist)
            try:
                times = np.load(filename)
            except Exception as e:
                print(e)
                times = scalibility(fn, dims, time_reps, num_datapoints, data_dist)
                np.save(filename, times)
            print(times)
            plt.plot(dims, times)

        plt.xlabel('Dimensionality')
        plt.ylabel('Time taken to execute (s)')
        plt.legend(fns)

        # saving with log-scale x-axis
        plt.xscale('log')
        plt.tight_layout()
        plt.savefig('log_scalability_{}.png'.format(data_dist))
        #plt.show()


"""
#### Scalability - scalability.py
The time taken to execute the different information theoretic measures as a function of increasing dimensionality of the data was recorded. The following figure shows the average time taken over 1000 runs for the case where 10000 data points uniformly distributed in [0,1] were added and the different metrics were invoked. From the partial information decomposition metrics, only synergy has been reported because estimating synergy involves estimation of total mutual information, redundant information and unique information twice (once for each source). Note that a uniform distribution likely causes data to cover the entire data space hence demonstrates the worst case scenario for this application where the sparse representation cannot be taken advantage of. In this case the application shows a linear increase in log scale of the time axis with a drop for 1024 dimensions. The reason for this is still under investigation.

On the other hand, when the data was normally distributed with mean 0.5, and standard deviation 0.1, the software could potentially take advantage of the sparse representation and the following figure shows the time taken to invoke the different metrics under this condition.
"""
