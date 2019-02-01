import numpy as np
import infotheory

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    TEST_HEADER = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

SUCCESS = bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC
FAILED = bcolors.FAIL + "FAILED" + bcolors.ENDC

def _except(e):
    print("\n" + FAILED)
    print(e)

def synergy_test(dims, nreps, nbins, data_ranges, data, results):
    try:
        # creating the object
        it = infotheory.InfoTools(dims,nreps)
        it.set_equal_interval_binning(nbins,data_ranges[0],data_ranges[1])
        # adding points
        it.add_data(data)
        # estimating mutual information
        redundant_info = it.redundant_info([1,2,0])
        unique_1 = it.mutual_info([0,-1,1]) - redundant_info
        unique_2 = it.mutual_info([-1,0,1]) - redundant_info
        synergy = it.synergy([1,2,0])
        if all(np.round([redundant_info, unique_1, unique_2, synergy], decimals=2) == results):
            print(synergy, SUCCESS)
        else:
            raise Exception("PID computation error")
    except Exception as e:
        _except(e)


def uniform_random_mi_test(dims, nreps, nbins, data_ranges, num_samples=1000):
    print('Testing mutual info with uniform random variables. MI = ', end='', flush=True)
    try:
        # creating the object
        it = infotheory.InfoTools(dims,nreps)
        it.set_equal_interval_binning(nbins,data_ranges[0],data_ranges[1])

        # adding points
        it.add_data(np.random.rand(num_samples,dims))
        # ...alternatively,
        #for _ in range(num_samples):
        #    it.add_data_point(np.random.rand(dims))

        # estimating mutual information
        mi = it.mutual_info([0,1])/((1/dims)*np.log2(np.prod(nbins)))
        print(mi, SUCCESS)

    except Exception as e:
        print(e)
        _except(e)

def identical_random_mi_test(dims, nreps, nbins, data_ranges, add_noise=False, num_samples=1000):
    print('Testing mutual info with identical random variables', end='', flush=True)
    if add_noise: print(' with noise. MI = ', end='', flush=True)
    else: print('. MI = ', end='', flush=True)

    try:
        # creating the object
        if dims%2!=0: dims+=1
        it = infotheory.InfoTools(dims,nreps)
        it.set_equal_interval_binning(nbins,data_ranges[0],data_ranges[1])
        p_dims = int(dims/2)

        # adding points
        for _ in range(num_samples):
            point1 = np.random.rand(p_dims)
            if add_noise: point2 = point1+(np.random.rand(p_dims)/30)
            else: point2 = point1
            it.add_data_point(np.concatenate((point1, point2)))

        # computing mutual information
        mi = it.mutual_info([0,1])/((1/dims)*np.log2(np.prod(nbins)))
        print(mi, SUCCESS)

    except Exception as e:
        _except(e)

def entropy_test(dims, nreps, nbins, data_ranges, data_sampler, num_samples=1000):
    try:
        # creating the object
        it = infotheory.InfoTools(dims,nreps)
        it.set_equal_interval_binning(nbins,data_ranges[0],data_ranges[1])
        # adding points
        for _ in range(num_samples):
            it.add_data_point([data_sampler()])
        # estimate entropy
        print(it.entropy([0]), SUCCESS)
    except Exception as e:
        _except(e)

def test_synergy(dims, nreps, nbins, data_ranges):
    """ Testing synergy with AND gate and XOR gate"""
    print("\n"+bcolors.TEST_HEADER + "PID - SYNERGY" + bcolors.ENDC)
    # AND gate
    data = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]]
    print('Testing synergy with AND gate = ', end='', flush=True)
    synergy_test(dims, nreps, nbins, data_ranges, data, [0.31,0.,0.,0.5])
    # XOR gate
    data = [[0,0,0],[0,1,1],[1,0,1],[1,1,0]]
    print('Testing synergy with XOR gate = ', end='', flush=True)
    synergy_test(dims, nreps, nbins, data_ranges, data, [0.,0.,0.,1.])

def test_mutual_info(dims, nreps, nbins, data_ranges):
    """ Testing mutual information under three conditions
    1. two uniform random variables (low MI)
    2. two identical random variables (high MI)
    3. one ranom variable and a noisy version of the same (medium MI)
    """
    print("\n"+bcolors.TEST_HEADER + "MUTUAL INFORMATION" + bcolors.ENDC)
    uniform_random_mi_test(dims, nreps, nbins, data_ranges)
    identical_random_mi_test(dims, nreps, nbins, data_ranges, add_noise=False)
    identical_random_mi_test(dims, nreps, nbins, data_ranges, add_noise=True)

def test_entropy(dims, nreps, nbins, data_ranges):
    """ Testing entropy under two conditions
    1. A uniform random variable (high entropy)
    2. A gaussian with low std. dev. (low entropy)
    """
    print("\n"+bcolors.TEST_HEADER + "ENTROPY" + bcolors.ENDC)
    print('Testing entropy with uniform distribution = ', end='', flush=True)
    entropy_test(dims, nreps, nbins, data_ranges, lambda: np.random.uniform())
    print('Testing entropy with normal distribution = ', end='', flush=True)
    entropy_test(dims, nreps, nbins, data_ranges, lambda: np.random.normal(loc=0.5, scale=0.01))

def test_binning(dims, nreps, nbins, data_ranges):
    """ Test execution of both types of binning
    1. Equal interval
    2. Manual specification
    """
    print("\n"+bcolors.TEST_HEADER + "BINNING" + bcolors.ENDC)
    mi_eq = mi_mb = None
    # resetting for this test
    dims = 2
    # generating a commong set of datapoints
    datapoints = []
    for _ in range(1000):
        point1 = np.random.rand()
        point2 = point1+(np.random.rand()/30)
        datapoints.append([point1, point2])

    try:
        print("Estimating MI using equal interval binning = ", end="", flush=True)
        # Equal interval binning
        it = infotheory.InfoTools(dims,nreps)

        # set bin boundaries
        it.set_equal_interval_binning(nbins,data_ranges[0],data_ranges[1])

        # adding points
        it.add_data(datapoints)

        # computing mutual information
        mi_eq = it.mutual_info([0,1])
        print(mi_eq, SUCCESS)
    except Exception as e:
        _except(e)

    try:
        print("Estimating MI using manually specified binning = ", end="", flush=True)
        # Manual binning
        it = infotheory.InfoTools(dims,nreps)

        # set bin boundaries
        it.set_bin_boundaries([[0.3333,0.6666],[0.3333,0.6666]])

        # adding points
        it.add_data(datapoints)

        # computing mutual information
        mi_mb = it.mutual_info([0,1])
        print(mi_mb, SUCCESS)
    except Exception as e:
        _except(e)

    # mi_eq == mi_mb?
    if mi_eq is not None and mi_mb is not None:
        if np.round(mi_eq,decimals=4) == np.round(mi_mb,decimals=4):
            print("Both methods gave same result ", SUCCESS)
        else:
            _except("Both binning methods with same bin boundaries did not return the same value for the same dataset")
    else:
        _except("Unable to compare binning methods because one of them failed")

def test_creation(dims, nreps, nbins, data_ranges):
    print("Testing creating an object. ", end='', flush=True)
    try:
        # creating object
        it = infotheory.InfoTools(dims,nreps)
        it.set_equal_interval_binning(nbins,data_ranges[0],data_ranges[1])
        print(bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC)
    except Exception as e:
        _except(e)

def run_tests(dims, nreps, nbins, data_ranges):
    """ runs all tests """
    print("\nTest config: dims={}, nreps={}, nbins={}, mins={}, maxs={}".format(dims, nreps, nbins, data_ranges[0], data_ranges[1]))
    print(bcolors.HEADER + "************ Starting tests ************" + bcolors.ENDC)
    test_creation(dims, nreps, nbins, data_ranges)
    test_binning(dims, nreps, [3,3], data_ranges)
    test_entropy(1, nreps, [50], [[0],[1]])
    test_mutual_info(dims, nreps, nbins, data_ranges)
    test_synergy(3, nreps, [2]*3, [[0]*3,[1]*3]) # binary data
    print("\n" + bcolors.HEADER + "************ Tests completed ************" + bcolors.ENDC)

def manual_test(m,n):
    it = infotheory.InfoTools(2,1,[2,2],[0,0],[1,1])
    it.add_data([[0,0]]*m+[[1,1]]*n)
    print("m = ", m, " n = ", n, " MI = ", it.mutual_info([0,1]))

if __name__ == "__main__":
    dims = 2
    nreps = 0
    nbins = [50]*dims
    data_ranges = [[0]*dims, [1]*dims]
    #for m,n in zip([1,2,2,3,500,499,200],[1,1,2,2,500,500,500]):
    #    manual_test(m,n)
    run_tests(dims, nreps, nbins, data_ranges)
