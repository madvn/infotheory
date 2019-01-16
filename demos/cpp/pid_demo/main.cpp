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

void binary_pid(int dims, int nReps, int binCounts, TVector<TVector <double> >& data){
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

    // Creating the object
    InfoTools it(dims, nReps);
    it.setBinCounts(nBins);
    it.setDataRanges(mins, maxs);

    // adding the data
    it.addData(data);

    // Invoking information theoretic tools
    TVector<int> varIDs; // list to identify different vars in the data
    varIDs.SetBounds(1,dims);
    varIDs.FillContents(1);

    // Finding total information from both sources
    varIDs[3] = 0;
    double total_mi = it.mutualInfo(varIDs);
    cout << "Total information from both sources = " << total_mi << endl;

    varIDs[1] = 1; // first source for estimating synergy
    varIDs[2] = 2; // second source for estimating synergy
    varIDs[3] = 0; // target variable

    // Invoking redundant information
    double redunInfo = it.redundantInfo(varIDs);
    cout << "Redundant information from two sources = " << redunInfo << endl;

    // Invoking uniqueInfo for source 1
    double unq1 = it.uniqueInfo(varIDs);
    cout << "Unique information from source 1 = " << unq1 << endl;

    // Invoking uniqueInfo for source 2
    varIDs[1] = 2;
    varIDs[2] = 1;
    double unq2 = it.uniqueInfo(varIDs);
    cout << "Unique information from source 2 = " << unq2 << endl;

    // Invoking synergy from InfoTools.h
    double synergy = it.synergy(varIDs);
    cout << "Synergestic information from two inputs = " << synergy << endl;
}


int main(){

    // Setup
    int dims = 3; // dimensionality of all random vars combined
    int nReps = 1; // number of shifted binnings over which data is binned and averaged
    int binCounts = 2; // since data is going to be binary

    // Creating an empty list for now to represent all data
    TVector<TVector <double> > data;
    data.SetBounds(1,4); // total of 4 datapoints for 2 input logic gate
    for(int n=1; n<=4; n++){
        // setting size for each datapoint - 3 dimensions per datapoint
        data[n].SetBounds(1,3);
    }

    // Adding data - XOR gate - truth table
    data[1][1] = 0; data[1][2] = 0; data[1][3] = 0;
    data[2][1] = 0; data[2][2] = 1; data[2][3] = 1;
    data[3][1] = 1; data[3][2] = 0; data[3][3] = 1;
    data[4][1] = 1; data[4][2] = 1; data[4][3] = 0;

    cout << endl << "Invoking pid for XOR" << endl;
    binary_pid(dims, nReps, binCounts, data);

    // Adding data - OR gate - truth table
    data[1][1] = 0; data[1][2] = 0; data[1][3] = 0;
    data[2][1] = 0; data[2][2] = 1; data[2][3] = 1;
    data[3][1] = 1; data[3][2] = 0; data[3][3] = 1;
    data[4][1] = 1; data[4][2] = 1; data[4][3] = 1;

    cout << endl << "Invoking pid for OR" << endl;
    binary_pid(dims, nReps, binCounts, data);
}
