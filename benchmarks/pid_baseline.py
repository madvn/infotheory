###############################################################################
# Parital information decomposition baseline
#
# Madhavun Candadai
# Dec, 2018
#
# Partial information decomposition for XOR and AND gates
###############################################################################
import infotheory

# 2 input AND gate
print("2-input logical AND")
data = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]

# creating the object and adding data
it_and = infotheory.InfoTools(3, 0)
it_and.set_equal_interval_binning([2] * 3, [0] * 3, [1] * 3)
it_and.add_data(data)

# PID-ing
total_mi = it_and.mutual_info([0, 0, 1])
redundant_info = it_and.redundant_info([1, 2, 0])
unique_1 = it_and.unique_info([1, 2, 0])
unique_2 = it_and.unique_info([2, 1, 0])
synergy = it_and.synergy([1, 2, 0])

print("total_mi = {}".format(total_mi))
print("redundant_info = {}".format(redundant_info))
print("unique_1 = {}".format(unique_1))
print("unique_2 = {}".format(unique_2))
print("synergy = {}\n".format(synergy))


# 2 input xor gate
print("2-input logical XOR")
data = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]

# creating the object and adding data
it_xor = infotheory.InfoTools(3, 0)
it_xor.set_equal_interval_binning([2] * 3, [0] * 3, [1] * 3)
it_xor.add_data(data)

# PID-ing
total_mi = it_xor.mutual_info([0, 0, 1])
redundant_info = it_xor.redundant_info([1, 2, 0])
unique_1 = it_xor.unique_info([1, 2, 0])
unique_2 = it_xor.unique_info([1, 2, 0])
synergy = it_xor.synergy([1, 2, 0])

print("total_mi = {}".format(total_mi))
print("redundant_info = {}".format(redundant_info))
print("unique_1 = {}".format(unique_1))
print("unique_2 = {}".format(unique_2))
print("synergy = {}\n".format(synergy))


# 3 input OR
print("3-input logical AND")
data = [
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 1],
]

# creating the object and adding data
it_3and = infotheory.InfoTools(4, 0)
it_3and.set_equal_interval_binning([2] * 4, [0] * 4, [1] * 4)
it_3and.add_data(data)

# PID-ing
# NOTE: The terms estimated below do not represent the 18 terms 
# of the 3 source PID decomposition. This is just an example of
# some of the different things you could do with the dataset. 
# For instance, redundant_12 is just the two variable redundant
# info between var==1 and var==2, and does not consider var==3
total_mi = it_3and.mutual_info([1, 1, 1, 0])
mi_12 = it_3and.mutual_info([1, 1, -1, 0])
mi_13 = it_3and.mutual_info([1, -1, 1, 0])
mi_23 = it_3and.mutual_info([-1, 1, 1, 0])
mi_1 = it_3and.mutual_info([1, -1, -1, 0])
mi_2 = it_3and.mutual_info([-1, 1, -1, 0])
mi_3 = it_3and.mutual_info([-1, -1, 1, 0])
redundant_info = it_3and.redundant_info([1, 2, 3, 0])
redundant_12 = it_3and.redundant_info([1, 2, -1, 0])
redundant_13 = it_3and.redundant_info([1, -1, 2, 0])
redundant_23 = it_3and.redundant_info([-1, 1, 2, 0])
unique_1 = it_3and.unique_info([1, 2, 3, 0])
unique_2 = it_3and.unique_info([2, 1, 3, 0])
unique_3 = it_3and.unique_info([2, 3, 1, 0])
synergy = it_3and.synergy([1, 2, 3, 0])
synergy_12 = it_3and.synergy([1, 2, -1, 0])
synergy_13 = it_3and.synergy([1, -1, 2, 0])
synergy_23 = it_3and.synergy([-1, 1, 2, 0])

print("total_mi = {}".format(total_mi))
print("mi_12 = {}".format(mi_12))
print("mi_13 = {}".format(mi_13))
print("mi_23 = {}".format(mi_23))
print("mi_1 = {}".format(mi_1))
print("mi_2 = {}".format(mi_2))
print("mi_3 = {}".format(mi_3))
print("redundant_info = {}".format(redundant_info))
print("redundant_12 = {}".format(redundant_12))
print("redundant_13 = {}".format(redundant_13))
print("redundant_23 = {}".format(redundant_23))
print("unique_1 = {}".format(unique_1))
print("unique_2 = {}".format(unique_2))
print("unique_3 = {}".format(unique_3))
print("synergy = {}".format(synergy))
print("synergy_12 = {}".format(synergy_12))
print("synergy_13 = {}".format(synergy_13))
print("synergy_23 = {}\n".format(synergy_23))

# 4 var multivariate analyses
print("3-input Even parity")
data = [
    [0, 0, 0, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 1],
]
# creating the object and adding data
it_par = infotheory.InfoTools(4, 0)
it_par.set_equal_interval_binning([2] * 4, [0] * 4, [1] * 4)
it_par.add_data(data)

# PID-ing
# NOTE: The terms estimated below do not represent the 18 terms 
# of the 3 source PID decomposition. This is just an example of
# some of the different things you could do with the dataset. 
# For instance, redundant_12 is just the two variable redundant
# info between var==1 and var==2, and does not consider var==3
total_mi = it_par.mutual_info([1, 1, 1, 0])
redundant_info = it_par.redundant_info([1, 2, 3, 0])
redundant_12 = it_par.redundant_info([1, 2, -1, 0])
redundant_13 = it_par.redundant_info([1, -1, 2, 0])
redundant_23 = it_par.redundant_info([-1, 1, 2, 0])
unique_1 = it_par.unique_info([1, 2, 3, 0])
unique_2 = it_par.unique_info([2, 1, 3, 0])
unique_3 = it_par.unique_info([2, 3, 1, 0])
synergy = it_par.synergy([1, 2, 3, 0])
synergy_12 = it_par.synergy([1, 2, -1, 0])
synergy_13 = it_par.synergy([1, -1, 2, 0])
synergy_23 = it_par.synergy([-1, 1, 2, 0])

print("total_mi = {}".format(total_mi))
print("redundant_info = {}".format(redundant_info))
print("redundant_12 = {}".format(redundant_12))
print("redundant_13 = {}".format(redundant_13))
print("redundant_23 = {}".format(redundant_23))
print("unique_1 = {}".format(unique_1))
print("unique_2 = {}".format(unique_2))
print("unique_3 = {}".format(unique_3))
print("synergy = {}".format(synergy))
print("synergy_12 = {}".format(synergy_12))
print("synergy_13 = {}".format(synergy_13))
print("synergy_23 = {}".format(synergy_23))
