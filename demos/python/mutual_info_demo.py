##############################################################################
# Infotheory demo to estimate MI between two 2D random vars
# https://github.iu.edu/madcanda/Infotheory
# Python demo
# Madhavun Candadai
# Nov 2018
##############################################################################
import infotheory
import numpy as np

## Setup
dims = 4  # total dimensionality of all variables = 2+2 = 4
nreps = 1 # number of shifted binnings over which data is binned and averaged
nbins = [10]*dims # number of bins along each dimension of the data
mins = [0]*dims # min value or left edge of binning for each dimension
maxs = [1]*dims # max value or right edge of binning for each dimension

## Creating object
it = infotheory.InfoTools(dims, nreps, nbins, mins, maxs)

## Adding data - concatenate data from all vars
for _ in range(100):
    it.add_data_point(np.random.rand(dims))

## Invoke infotheory tools
varIDs = [0,0,1,1] # to identify the different vars
mi = it.mutual_info(varIDs) # mutual information between two random vars
mi /= np.log2(np.prod(nbins)) # normalizing
print('Mutual information between the two random 2D data = {}'.format(mi))

varIDs = [0,-1,1,-1] # dimensions marked anything other than 0 or 1 are ignored for mutual information
mi = it.mutual_info(varIDs) # mutual information between first dimension two 2D random vars
mi /= np.log2(np.prod(nbins)) # normalizing
print('Mutual information between first dimension of two random 2D data = {}'.format(mi))
