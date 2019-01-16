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

__version__ = "1.0"
class InfoTools(object):
    """ Python Wrapper class for InfoTools.h

    This class loads the .so file from the compiled InfoTools.h that allows functions written in C++ to be called from Python. Create and object of this class to call associated functions.
    """
    def __init__(self, dims, nreps, nbins, mins, maxs):
        """ reads in .so file and creates object of InfoTools cpp class

        ARGS
        dims: (int) total dimensionality of all variables
        nreps: (int) number of shifted binnings over which data is binned and averaged
        nbins: (list-like, size=dims) number of bins along each dimension of the data
        mins: (list-like, size=dims) min value or left edge of binning for each dimension
        maxs: (list-like, size=dims) max value or right edge of binning for each dimension
        """
        dll_dir = '/'.join(os.path.dirname(__file__).split('/')[:-1])
        dll_file = glob.glob(os.path.join(dll_dir,"infotheoryClass*.so"))[0]
        self.libc = cdll.LoadLibrary(dll_file)

        # creating object of cpp class
        class_ctor_wrapper = self.libc.InfoTools_new
        class_ctor_wrapper.argtypes = [c_int, c_int]
        class_ctor_wrapper.restype = c_void_p
        self._obj = c_void_p(class_ctor_wrapper(dims, nreps))

        # config
        self._set_bin_counts(nbins)
        self._set_data_ranges(mins, maxs)

    #****************
    # Inspection utils
    #****************
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

    #****************
    # Data handlers
    #****************
    def _set_bin_counts(self, nbins):
        """ (internal use only) set the number of bins along each dimension"""
        setBinCounts_wrapper = self.libc.setBinCounts_c_wrapper
        setBinCounts_wrapper.argtypes = [c_void_p, py_object]
        setBinCounts_wrapper(self._obj, list(nbins))

    def _set_data_ranges(self, mins, maxs):
        """ (internal use only) set min and max for each dimension """
        setDataRanges_wrapper = self.libc.setDataRanges_c_wrapper
        setDataRanges_wrapper.argtypes = [c_void_p, py_object, py_object]
        setDataRanges_wrapper(self._obj, list(mins), list(maxs))

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

    #****************
    # Info theory tools
    #****************
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
        """ Compute redundant information about a random var from two random vars for datapoints that have already been added.
        The target random var is identified by varIDs==0
        The two sources are identified by varIDs==1 and varIDs==2.
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Redundant information from vars defined by varIDs==1 and varIDs==2 about varIDs==0

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
        """ Compute unique information about a random var from two random vars for datapoints that have already been added.
        The target random var is identified by varIDs==0
        The two sources are identified by varIDs==1 and varIDs==2.
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Unique information from vars defined by varIDs==1 about varIDs==0 that is not redundant with varIDs==2

        Example:
        if dims = 4, 4D datapoints will be added. If the first dimension denotes the target and the second and third denote the two sources, then set
        varIDs = [0,1,2,-1]
        """
        uniqueInfo_wrapper = self.libc.uniqueInfo_c_wrapper
        uniqueInfo_wrapper.argtypes = [c_void_p, py_object]
        uniqueInfo_wrapper.restype = c_double
        return uniqueInfo_wrapper(self._obj, list(var_IDs))

    def synergy(self, var_IDs):
        """ Compute synergistic information about a random var from two random vars for datapoints that have already been added.
        The target random var is identified by varIDs==0
        The two sources are identified by varIDs==1 and varIDs==2.
        Set varIDs=-1 for dimensions to be ignored.

        ARGS:
        varIDs: (list-like, size=dims) list of length equal to dimensionality of data

        RETURNS:
        Synergistic information from vars defined by varIDs==1 and varIDs==2 about varIDs==0

        Example:
        if dims = 4, 4D datapoints will be added. If the first dimension denotes the target and the second and third denote the two sources, then set
        varIDs = [0,1,2,-1]
        """
        synergy_wrapper = self.libc.synergy_c_wrapper
        synergy_wrapper.argtypes = [c_void_p, py_object]
        synergy_wrapper.restype = c_double
        return synergy_wrapper(self._obj, list(var_IDs))
