##############################################################################
# Infotheory demo to estimate synergy in XOR and AND operations
# Python
# Madhavun Candadai
# Nov 2018
##############################################################################
import infotheory
import numpy as np

## Setup
dims = 3  # total dimensionality of all variables = 2 sources + 1 target = 3
nreps = 0 # number of shifted binnings over which data is binned and averaged
nbins = [2]*dims # number of bins along each dimension of the data = 2 for binary data
mins = [0]*dims # min value or left edge of binning for each dimension
maxs = [1]*dims # max value or right edge of binning for each dimension

## Creating object
it_xor = infotheory.InfoTools(dims, nreps)
it_xor.set_equal_interval_binning(nbins, mins, maxs)

## Adding data for XOR
it_xor.add_data([[0,0,0],
                [0,1,1],
                [1,0,1],
                [1,1,0]
                ])

# display config
it_xor.display_config()

## Invoking info theoretic functions
xor_synergy = it_xor.synergy([1,2,0])


## Creating object
it_and = infotheory.InfoTools(dims, nreps)
it_and.set_equal_interval_binning(nbins, mins, maxs)

## Adding data for AND
it_and.add_data([[0,0,0],
                [0,1,0],
                [1,0,0],
                [1,1,1]
                ])
                
# display config
it_and.display_config()

## Invoking info theoretic functions
and_synergy = it_and.synergy([1,2,0])

print('Synergy between inputs in a binary XOR gate = {}'.format(xor_synergy))
print('Synergy between inputs in a binary AND gate = {}'.format(and_synergy))
