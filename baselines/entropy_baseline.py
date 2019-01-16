###############################################################################
# Entropy baseline
#
# Madhavun Candadai
# Dec, 2018
#
# Entropy of a coin flip for different probabilities of HEADS ranging from 0 to
# 1 should give an inverted-U shaped curve
###############################################################################

import numpy as np
import infotheory
import matplotlib.pyplot as plt

# range of probabilties for HEADS in coin flip
p = np.arange(0,1.01,0.01)
entropies = []
for pi in p:
    it = infotheory.InfoTools(1, 1, [2], [0], [1])

    # flipping coin 10000 times
    for _ in range(10000):
        if np.random.rand()<pi: it.add_data_point([0])
        else: it.add_data_point([1])

    # estimating entropy
    entropies.append(it.entropy([0]))

plt.figure(figsize=[3,2])
plt.plot(p, entropies)
plt.xlabel('Probability of HEADS')
plt.ylabel('Entropy')
plt.tight_layout()
#plt.savefig('./entropy_baseline.png')
plt.show()
