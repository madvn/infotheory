# -*- coding: utf-8 -*-
""" @package doscstring
Infotheory - information theoretic analysis.

Contains InfoTools class that allows estimation of
1. Entropy
2. Mutual Information
3. Partial Information Decomposition measures
    a. Unique Information
    b. Redundant Information
    c. Synergy
"""
import os
import glob
from ctypes import cdll, c_void_p, c_int, py_object, py_object, c_double

__version__ = "1.0.1"


class InfoTools(object):
    """ Python Wrapper class for InfoTools.h

    This class loads the .so file from the compiled InfoTools.h that allows functions written in C++ to be called from Python. Create and object of this class to call associated functions.
    """

    def __init__(self, dims, nreps=0):
        """ reads in .so file and creates object of InfoTools cpp class

        ARGS
        dims: (int) total dimensionality of all variables
        nreps: (int) number of shifted binnings over which data is binned and averaged
        """
        self.dims = dims
        dll_dir = "/".join(os.path.dirname(__file__).split("/")[:-1])
        dll_file = glob.glob(os.path.join(dll_dir, "infotheoryClass*.so"))[0]
        self.libc = cdll.LoadLibrary(dll_file)

        # creating object of cpp class
        class_ctor_wrapper = self.libc.InfoTools_new
        class_ctor_wrapper.argtypes = [c_int, c_int]
        class_ctor_wrapper.restype = c_void_p
        self._obj = c_void_p(class_ctor_wrapper(dims, nreps))

    # ****************
    # Inspection utils
    # ****************
    def display_config(self):
        """ Display the config for analyses such as number of bins, dimensionality etc. """
        displayConfig_wrapper = self.libc.displayConfig_c_wrapper
        displayConfig_wrapper.argtypes = [c_void_p]
        displayConfig_wrapper(self._obj)

    def display_snapshot(self):
        """ Display current status such as number of points added, number of non-empty bins etc. """
        displaySnapshot_wrapper = self.libc.displaySnapshot_c_wrapper
        displaySnapshot_wrapper.argtypes = [c_void_p]
        displaySnapshot_wrapper(self._obj)

    # ****************
    # Binning methods
    # ****************
    def set_equal_interval_binning(self, nbins, mins, maxs):
        """ set binning mode to be equal interval binning

        ARGS
        nbins: (list,length=dims) list with the number of bins along each dimension
        mins: (list,length=dims) list with the minimum values along each dimension
        maxs: (list,length=dims) list with the maximum values along each dimension
        """
        setEqualIntervalBinning_wrapper = self.libc.setEqualIntervalBinning_c_wrapper
        setEqualIntervalBinning_wrapper.argtypes = [
            c_void_p,
            py_object,
            py_object,
            py_object,
        ]
        setEqualIntervalBinning_wrapper(self._obj, list(nbins), list(mins), list(maxs))

    def set_bin_boundaries(self, boundaries, dim_index=None):
        """ set the left margin of each bin for each dimension

        ARGS
        boundaries: a list with a list of bin-margins for each dimension OR a list for just one dimension with dimension specified in dim_index.\n
                Length of list = number_of_bins-1, left most bin is (-inf,list[0]) and right most bin is (list[-1],inf)
        dim_index: (int, default=None) denoting the dimension for which the bins are being set, if boundaries is a single list of boundaries
        """
        set_bin_boundaries_wrapper = self.libc.setBinBoundaries_c_wrapper
        set_bin_boundaries_wrapper.argtypes = [c_void_p, py_object, c_int]
        if dim_index:
            set_bin_boundaries_wrapper(self._obj, list(boundaries), int(dim_index))
        else:
            assert (
                len(boundaries) == self.dims
            ), "ERROR: boundaries should be a list of length = total dimensionality = {}, or provide dim_index".format(
                self.dims
            )
            for dim_ind, boundary_list in enumerate(boundaries):
                set_bin_boundaries_wrapper(self._obj, list(boundary_list), int(dim_ind))

    # ****************
    # Data handlers
    # ****************
    def add_data_point(self, datapoint):
        """ add one data point to analyses

        ARGS
        datapoint: (list-like, size=dims) the datapoint to be added
        """
        addDataPoint_wrapper = self.libc.addDataPoint_c_wrapper
        addDataPoint_wrapper.argtypes = [c_void_p, py_object]
        addDataPoint_wrapper(self._obj, list(datapoint))

    def add_data(self, data):
        """ add several data points at once

        ARGS
        data: (list-like, size=[number_of_datapoints, dims]) list of datapoints to be added
        """
        for datapoint in data:
            self.add_data_point(datapoint)

    def clearAllData(self):
        """ clear all data added so far and start afresh

        It is recommended to create a new object instead
        """
        clearAllData_wrapper = self.libc.clearAllData_c_wrapper
        clearAllData_wrapper.argtypes = [c_void_p]
        clearAllData_wrapper(self._obj)

    def __del__(self):
        """ deletes the cpp pointer """
        delete_ptr_wrapper = self.libc.delete_instance_of_class
        delete_ptr_wrapper.argtypes = [c_void_p]
        delete_ptr_wrapper.restype = c_void_p
        delete_ptr_wrapper(self._obj)

    # ****************
    # Info theory tools
    # ****************
    def entropy(self, var_IDs):
        """ Compute entropy of random vars given by varIDs==0

        ARGS:
        varIDs: (list-like, size=dims) list to identify the dimensions of the data that need to be considered to estimate entropy

        RETURNS:
        Entropy of random variable made up by data along dimensins where varIDs==0

        Example:
        if dims = 4, 4D datapoints will be added, but if only the first 2 dimensions make up the variable of interest, then set
        varIDs = [1,1,-1,-1]
        The dims with varID==-1 will be ignored
        """
        entropy_wrapper = self.libc.entropy_c_wrapper
        entropy_wrapper.argtypes = [c_void_p, py_object]
        entropy_wrapper.restype = c_double
        return entropy_wrapper(self._obj, list(var_IDs))

    def mutual_info(self, var_IDs):
        """ Compute mutual information between two random vars for datapoints that have already been added.
        The two variables are identified by varIDs==0 and varIDs==1.
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Mutual information between vars defined by varIDs==0 and varIDs==1

        Example:
        if dims = 4, 4D datapoints will be added, but if only the first 2 dimensions make up one variable and the rest the other, then set
        varIDs = [0,0,1,1]
        The dims with varID==-1 will be ignored
        """
        mutualInfo_wrapper = self.libc.mutualInfo_c_wrapper
        mutualInfo_wrapper.argtypes = [c_void_p, py_object]
        mutualInfo_wrapper.restype = c_double
        return mutualInfo_wrapper(self._obj, list(var_IDs))

    def redundant_info(self, var_IDs):
        """ Compute redundant information about a random var from two (or three) random vars for datapoints that have already been added.
        The target random var is identified by varIDs==0
        The sources are identified by varIDs==1 and varIDs==2 (optionally varIDs==3 in the case of three sources)
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Redundant information from vars defined by varIDs==1 and varIDs==2 (optionally varIDs==3 in the case of three sources) about varIDs==0

        Example:
        if dims = 4, 4D datapoints will be added. If the first dimension denotes the target and the second and third denote the two sources, then set
        varIDs = [0,1,2,-1]
        The dims with varID==-1 will be ignored
        """
        redundantInfo_wrapper = self.libc.redundantInfo_c_wrapper
        redundantInfo_wrapper.argtypes = [c_void_p, py_object]
        redundantInfo_wrapper.restype = c_double
        return redundantInfo_wrapper(self._obj, list(var_IDs))

    def unique_info(self, var_IDs):
        """ Compute unique information about a random var from two (or three) random vars for datapoints that have already been added.
        The target random var is identified by varIDs==0
        The sources are identified by varIDs==1 and varIDs==2 (optionally varIDs==3 in the case of three sources)
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Unique information from vars defined by varIDs==1 about varIDs==0 that is not redundant with varIDs==2 (or with varIDs==3 in the case of three sources)

        Example:
        if dims = 4, 4D datapoints will be added. If the first dimension denotes the target and the second and third denote the two sources, then set
        varIDs = [0,1,2,-1]
        """
        uniqueInfo_wrapper = self.libc.uniqueInfo_c_wrapper
        uniqueInfo_wrapper.argtypes = [c_void_p, py_object]
        uniqueInfo_wrapper.restype = c_double
        return uniqueInfo_wrapper(self._obj, list(var_IDs))

    def synergy(self, var_IDs):
        """ Compute synergistic information about a random var from two (or three) random vars for datapoints that have already been added.
        The target random var is identified by varIDs==0
        The sources are identified by varIDs==1 and varIDs==2 (optionally varIDs==3 in the case of three sources)
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Synergistic information from vars defined by varIDs==1 and varIDs==2 (and varIDs==3 in the case of three sources) about varIDs==0

        Example:
        if dims = 4, 4D datapoints will be added. If the first dimension denotes the target and the second and third denote the two sources, then set
        varIDs = [0,1,2,-1]
        """
        synergy_wrapper = self.libc.synergy_c_wrapper
        synergy_wrapper.argtypes = [c_void_p, py_object]
        synergy_wrapper.restype = c_double
        return synergy_wrapper(self._obj, list(var_IDs))
