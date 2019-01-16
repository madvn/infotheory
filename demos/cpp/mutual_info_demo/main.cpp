//**************************************************************************//
// Infotheory demo to estimate MI between two 2D random vars
// C++
// Madhavun Candadai
// Nov 2018
//**************************************************************************//
#include <iostream>
#include <math.h>
#include "VectorMatrix.h"
#include "InfoTools.h"

using namespace std;

double D_RAND_MAX = RAND_MAX; // typecasting to double

int main(){

    // Setup
    int dims = 4; // dimensionality of all random vars combined
    int nReps = 1; // number of shifted binnings over which data is binned and averaged
    int binCounts = 10;
    // number of bins along each dimension of the data
    TVector<int> nBins; // declaring TVector list
    nBins.SetBounds(1,dims); // defining bounds
    nBins.FillContents(binCounts); // filling all places
    // min value or left edge of binning for each dimension
    TVector<double> mins;
    mins.SetBounds(1,dims);
    mins.FillContents(0.);
    // max value or right edge of binning for each dimension
    TVector<double> maxs;
    maxs.SetBounds(1,dims);
    maxs.FillContents(1.);
    // Creating an empty list for now to represent the datapoint
    TVector<double> datapoint;
    datapoint.SetBounds(1,dims);

    // Creating the object
    InfoTools it(dims, nReps);
    it.setBinCounts(nBins);
    it.setDataRanges(mins, maxs);
    it.displayConfig();

    // Adding data
    for(int n=0; n<10000; n++){
        // create a random datapoint
        for(int d=1; d<=dims; d++){// since bounds for datapoint is [1,dims]
            datapoint[d] = rand()/D_RAND_MAX;
        }
        it.addDataPoint(datapoint);
        if(n%1000==0){
            it.displaySnapshot();
        }
    }

    // Invoking information theoretic tools
    TVector<int> varIDs; // list to identify different vars in the data
    varIDs.SetBounds(1,dims);
    varIDs[1] = 0; varIDs[2] = 1; // random var 1 is along dims 1 and 2
    varIDs[3] = 1; varIDs[4] = 1; // random var 2 is along dims 3 and 4

    // Computing mutual info between random var 1 and random var 2
    double mi = it.mutualInfo(varIDs);
    mi /= log2(binCounts);
    cout << "Mutual information between the two random 2D data = " << mi << endl;
    it.displaySnapshot();

    // changing varID to find mutual info between dim 1 of var 1 and var2
    varIDs[1] = 0; varIDs[2] = 1; // -1 will cause that dim to be ignored
    varIDs[3] = 1; varIDs[4] = -1;

    // Computing mutual info between dim 1 of two 2D random vars
    mi = it.mutualInfo(varIDs);
    mi /= log2(binCounts);
    cout << "Mutual information between first dimension of two random 2D data = " << mi << endl;
    it.displaySnapshot();
}
