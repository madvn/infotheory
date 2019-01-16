###############################################################################
# Parital information decomposition baseline
#
# Madhavun Candadai
# Dec, 2018
#
# Partial information decomposition for XOR and AND gates
###############################################################################
import infotheory

# 2 input xor gate
data = [[0,0,0],[0,1,1],[1,0,1],[1,1,0]]

# creating the object and adding data
it_xor = infotheory.InfoTools(3, 1, [2]*3, [0]*3, [1]*3)
it_xor.add_data(data)

# PID-ing
print("2-input XOR")
total_mi = it_xor.mutual_info([0,0,1])
redundant_info = it_xor.redundant_info([1,2,0])
unique_1 = it_xor.unique_info([1,2,0])
unique_2 = it_xor.unique_info([1,2,0])
synergy = it_xor.synergy([1,2,0])
print("total_mi = {}".format(total_mi))
print("redundant_info = {}".format(redundant_info))
print("unique_1 = {}".format(unique_1))
print("unique_2 = {}".format(unique_2))
print("synergy = {}\n".format(synergy))


# 2 input AND gate
data = [[0,0,0],[0,1,0],[1,0,0],[1,1,1]]

# creating the object and adding data
it_and = infotheory.InfoTools(3, 1, [2]*3, [0]*3, [1]*3)
it_and.add_data(data)

# PID-ing
print("2-input AND")
total_mi = it_and.mutual_info([0,0,1])
redundant_info = it_and.redundant_info([1,2,0])
unique_1 = it_and.unique_info([1,2,0])
unique_2 = it_and.unique_info([2,1,0])
synergy = it_and.synergy([1,2,0])
print("total_mi = {}".format(total_mi))
print("redundant_info = {}".format(redundant_info))
print("unique_1 = {}".format(unique_1))
print("unique_2 = {}".format(unique_2))
print("synergy = {}\n".format(synergy))
