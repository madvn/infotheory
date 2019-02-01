#include <Python.h>
#include "VectorMatrix.h"
#include "InfoTools.h"

extern "C"
{
    // __init__ or constructor
    InfoTools* InfoTools_new(int dims, int nreps){return new InfoTools(dims, nreps);}

    // destructor
    void delete_instance_of_class(InfoTools* ptr){
        try{
            delete ptr;
        }
        catch (const std::exception& e) {
            std::cout << "Exception caught while trying to delete pointer " << std::endl << e.what() << std::endl;
        }
    }

    /****************
    local utils
    ****************/
    void to_tvector_int(TVector<int> &linkerList, PyObject* arg){
        // get reference to pyobject and map to tvector reference
        int count = PyList_GET_SIZE(arg);
        linkerList.SetBounds(1,count);
        for (int i=0; i<count; i++) {
            linkerList[i+1] = PyLong_AsLong(PyList_GET_ITEM(arg,i));
        }
    }
    void to_tvector_double(TVector<double> &linkerList, PyObject* arg){
        // get reference to pyobject and map to tvector reference
        int count = PyList_GET_SIZE(arg);
        linkerList.SetBounds(1,count);
        for (int i=0; i<count; i++) {
            linkerList[i+1] = PyFloat_AsDouble(PyList_GET_ITEM(arg,i));
        }
    }

    /****************
    inspection tools
    ****************/
    void displayConfig_c_wrapper(InfoTools* it){
        it->displayConfig();
    }
    void displaySnapshot_c_wrapper(InfoTools* it){
        it->displaySnapshot();
    }

    /****************
    binning methods
    ****************/
    void setEqualIntervalBinning_c_wrapper(InfoTools* it, PyObject* nbins, PyObject* mins, PyObject* maxs){
        TVector<int> t_nbins;
        to_tvector_int(t_nbins, nbins);
        TVector<double> t_mins, t_maxs;
        to_tvector_double(t_mins, mins);
        to_tvector_double(t_maxs, maxs);
        it->setEqualIntervalBinning(t_nbins, t_mins, t_maxs);
    }
    void setBinBoundaries_c_wrapper(InfoTools* it, PyObject* boundaries, int dim_index){
        TVector<double> t_boundaries;
        to_tvector_double(t_boundaries, boundaries);
        it->setBinBoundaries(t_boundaries, dim_index);
    }

    /****************
    data handlers
    ****************/
    void addDataPoint_c_wrapper(InfoTools* it, PyObject* dataPoint){
        TVector<double> t_dataPoint;
        to_tvector_double(t_dataPoint, dataPoint);
        it->addDataPoint(t_dataPoint);
    }
    void clearAllData_c_wrapper(InfoTools* it){
        it->clearAllData(); // TODO
    }

    /****************
    info theory tools
    ****************/
    PyObject* entropy_c_wrapper(InfoTools* it, PyObject* varIDs){
        TVector<int> t_varIDs;
        to_tvector_int(t_varIDs, varIDs);
        return PyFloat_FromDouble(it->entropy(t_varIDs));
    }
    PyObject* mutualInfo_c_wrapper(InfoTools* it, PyObject* varIDs){
        TVector<int> t_varIDs;
        to_tvector_int(t_varIDs, varIDs);
        return PyFloat_FromDouble(it->mutualInfo(t_varIDs));
    }
    PyObject* redundantInfo_c_wrapper(InfoTools* it, PyObject* varIDs){
        TVector<int> t_varIDs;
        to_tvector_int(t_varIDs, varIDs);
        return PyFloat_FromDouble(it->redundantInfo(t_varIDs));
    }
    PyObject* uniqueInfo_c_wrapper(InfoTools* it, PyObject* varIDs){
        TVector<int> t_varIDs;
        to_tvector_int(t_varIDs, varIDs);
        return PyFloat_FromDouble(it->uniqueInfo(t_varIDs));
    }
    PyObject* synergy_c_wrapper(InfoTools* it, PyObject* varIDs){
        TVector<int> t_varIDs;
        to_tvector_int(t_varIDs, varIDs);
        return PyFloat_FromDouble(it->synergy(t_varIDs));
    }
}
