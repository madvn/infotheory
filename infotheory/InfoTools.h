/******************************************************/
// A Data handler class that deals with binning and
// computing probabilities
//
// Created - March, 2018 - MCV
/******************************************************/

#include <iostream>
#include <math.h>
#include "VectorMatrix.h"

#pragma once
#define TESTMODE 0

class InfoTools{
    // making everything public to make testing easier
    #if !TESTMODE
    private:
    #else
    public:
    #endif
        int BIN_LIMIT;
        // numShifts(numDims(numBins))
        // to allow different number of bins along different dimensions
        TVector<TVector<TVector<double> > > bins;

        // one matrix for data binned using one list of bins
        TVector<TMatrix<double> > binnedData; // XXX matrixShape=(None,numDims+1)

        // one matrix averaged across all shifts
        TMatrix<double> avgBinnedData;

        // one matrix for data binned using one list of bins
        //TVector<TMatrix<double> > probs; // all combinations of probabilities

        TVector<int> nBins; // number of bins along each dimension

        double totalPoints,totalAvgPoints;
        int nDims, nReps, dataLen;
        int dataInitedFlag, dataReadyFlag;
        TVector<int> binningInitedFlag;

    #if !TESTMODE
    public:
    #endif
        /*******************
        * Inits
        *******************/
        InfoTools(int dims, int nreps=0){
            //!Constructor
            /*! ARGS\n
            *     dims - dimensionality of data (all variables combined)\n
            *     nreps - number of reps on each side of bin boundary to compute average shifted histogram\n
            */
            BIN_LIMIT = 500;

            // resetting vars
            nDims = dims;
            nReps = nreps*2 + 1;
            dataLen = 0; // number of non-empty bins, across all shifts
            totalPoints = totalAvgPoints = 0;

            bins.SetBounds(1,nReps);
            for(int r=1; r<=nReps; r++){
                // bins[r] is all bins for a particular shift
                bins[r].SetBounds(1,nDims);
            }
            binnedData.SetBounds(1,nReps);

            nBins.SetBounds(1,dims);
            nBins.FillContents(0.);

            //cout << "nBins = " << nBins <<endl;

            // flag set
            dataInitedFlag = 0;
            dataReadyFlag = 0;
            binningInitedFlag.SetBounds(1,nDims);
            binningInitedFlag.FillContents(0.);

            //cout << "Total points = " << totalPoints << endl;
        }

        ~InfoTools(){};

        /*******************
        * Inspection tools
        *******************/

        //!Display the config for analyses such as number of bins, dimensionality etc.
        void displayConfig(){
            cout << "************************ CONFIG ************************" << endl;
            cout << "Total dimensionality = " << nDims << endl;
            cout << "Number of shifted bins = " << nReps << endl;
            cout << "Number of bins in each dimension = " << nBins << endl;
            cout << "Bin boundaries in each dimension:" << endl;
            for(int d=1; d<=nDims;d++){
                cout << "\tFor dimension #" << d << endl;
                for(int r=1; r<=nReps; r++){
                    cout << "\t\tFor rep #" << r << ":" << bins[r][d] <<endl;
                }
            }
            cout << "********************************************************" << endl;
        }

        //!Display current status such as number of points added, number of non-empty bins etc.
        void displaySnapshot(){
            cout << "************************ SNAPSHOT ************************" << endl;
            cout << "Number of total datapoints added = " << totalPoints << endl;
            cout << "Number of populated bins = " << dataLen << endl;
            if(!dataReadyFlag)
                cout << "Size of populated bin list = " << binnedData[1].ColumnSize() << endl;
            cout << "Has data been collapsed across multiple shifted binnings? " << (dataReadyFlag==0 ? "No":"Yes") << endl;
            if(dataReadyFlag)
                cout << "Size of average binned data = " << avgBinnedData.ColumnSize() << endl;
            cout << "**********************************************************" << endl;
        }

        /*******************
        * Binning schemes
        *******************/

        //!Set bounds on probs depending on max(ids)
        /*!     nbs - TVector with length=dims and has number of bins for each dimension\n
        *     mins - TVector with length=dims that has min on each dim\n
        *     maxs - TVector with length=dims that has max on each dim
        */
        void setEqualIntervalBinning(TVector<int>& nbs, TVector<double>& mins, TVector<double>& maxs){
            if(dataLen > 0){
                cerr << "ERROR: Cannot set bins after if at least one bin has been populated" << endl;
                exit(1);
            }
            // init bins[r][d] with shifted values from mins[d] to maxs[d] (left margin of bins)
            if(mins.Size() != nDims){
                cerr << "ERROR: 'mins' should be a list of length = total dimensionality = " << nDims << endl;
                exit(1);
            }
            if(maxs.Size() != nDims){
                cerr << "ERROR: 'maxs' should be a list of length = total dimensionality = " << nDims << endl;
                exit(1);
            }
            if(nbs.Size() != nDims){
                cerr << "ERROR: Bin counts should be a list of length = total dimensionality = " << nDims << endl;
                exit(1);
            }

            int b=nbs.LowerBound(), mi=mins.LowerBound(), ma=maxs.LowerBound();
            //cout << b << " " << mi << " " << ma << endl;
            for(int d=1; d<=nDims; d++){
                TVector<double> boundaries;
                boundaries.SetBounds(1,nbs[b]-1);
                for(int bo=1; bo<nbs[b]; bo++){
                    double boundary = mins[mi] + bo*(maxs[ma]-mins[mi])/nbs[b];
                    boundaries[bo] = boundary;
                }
                setBinBoundaries(boundaries, d-1);
                b++;mi++;ma++;
            }
        }

        //!Set left-boundaries for the binning of specified dimension
        /*!     boundaries - TVector that has bin-margins for specified dimension. Length of list = number_of_bins-1, left most bin is (-inf,list[0]) and right most bin is (list[-1],inf)
        *     dim_index - int with dimension of choice - 0-indexing
        */
        void setBinBoundaries(TVector<double> boundaries, int dimIndex){
            if(dataLen > 0){
                cerr << "ERROR: Cannot set bins after if at least one bin has been populated" << endl;
                exit(1);
            }
            int bLb = boundaries.LowerBound();
            int bUb = boundaries.UpperBound();
            dimIndex += 1; // indexing is 1 in this library
            nBins[dimIndex] = boundaries.Size()+1;
            int bi = nBins[dimIndex]-1;
            // if there is more than one rep, create empty bin boundary vecs for shifted binnings
            for(int r=1; r<=nReps; r++){
                // set bounds on bin TVecs
                bins[r][dimIndex].SetBounds(1,bi);
            }

            // first setting for 1 rep
            for(int b=1,b1=bLb; b<=bi; b++,b1++){
                bins[1][dimIndex][b] = boundaries[b1];
            }

            // now for the other reps
            double offsetWidth, maxLimit;
            TVector<double> unitOffset, minLimit;
            unitOffset.SetBounds(1,bi);
            minLimit.SetBounds(1,bi);
            for(int b=1,b1=bLb; b<bi; b++,b1++){
                offsetWidth = (boundaries[b1+1]-boundaries[b1])/2;
                minLimit[b] = boundaries[b1]-offsetWidth;
                //maxLimit = boundaries[b1]+offsetWidth;
                unitOffset[b] = (boundaries[b1] - minLimit[b])/(((nReps-1)/2)+1);
            }
            // // setting last bin separately using same offset as last but one
            minLimit[bi] = boundaries[bUb] - offsetWidth;
            unitOffset[bi] = (boundaries[bUb] - minLimit[bi])/(((nReps-1)/2)+1);

            int r;
            // for each rep to the left of boundaries
            for(r=2; r<=((nReps-1)/2)+1; r++){
                // for each bin
                for(int b=1,b1=bLb; b<=bi; b++,b1++){
                    bins[r][dimIndex][b] = boundaries[b1] - unitOffset[b]*(r-1);
                    //cout << bins[r][d][b] << " ";
                }
            }
            // for each rep to the right of boundaries
            for(r=((nReps-1)/2)+2; r<=nReps; r++){
                // for each bin
                for(int b=1,b1=bLb; b<=bi; b++,b1++){
                    bins[r][dimIndex][b] = boundaries[b1] + unitOffset[b]*(r-1);
                    //cout << bins[r][d][b] << " ";
                }
            }
            binningInitedFlag[dimIndex] = 1;
        }

        //!Set left-boundaries for the binning of all dimensions
        /*!     boundaries - TVector that has TVectors for left-margin of all dims. Length of each TVector = number_of_bins-1, left most bin is (-inf,list[0]) and right most bin is (list[-1],inf)
        */
        void setBinBoundaries(TVector<TVector <double> > boundaries){
            if(boundaries.Size() != nDims){
                cerr << "ERROR: Boundaries should be a list of length = total dimensionality = " << nDims << endl;
                exit(1);
            }
            int di=1;
            for(int d=boundaries.LowerBound(); d<=boundaries.UpperBound(); d++){
                setBinBoundaries(boundaries[d], di-1); // due to 0-indexing of dims in setBinBoundaries
                di++;
            }
        }

        /*******************
        * Data Handler
        *******************/
        //!Identify bin for given datapoint and add to count of points in that bin
        /*!     dataPoint - TVector with length=dims contains the datapoint to be added
        */
        void addDataPoint(TVector<double>& dp){
            for(int d=1; d<=nDims; d++){
                if(binningInitedFlag[d] == 0){
                    cerr << "ERROR: binning has not been specified for dimension " << d-1 << " (0-indexing)" << endl;
                    exit(1);
                }
            }
            if(dataReadyFlag){
                cout << "WARNING: Datapoint is being added after existing collapsing binned data. Previous datapoints will be lost." << endl;
                cout << "All datapoints need to be added first before using any information theoretic tools" << endl;
            }
            if(dp.Size() != nDims){
                cerr << "ERROR: Each datapoint must be of size = total dimensionality = " << nDims << " *** ";
                cerr << "Skipping this datapoint" << endl;
                return;
            }

            // renormalizing bounds
            TVector<double> dataPoint;
            normalizeBounds(dataPoint, dp);

            dataReadyFlag = 0;
            totalPoints++;
            // locate bin and update counts
            // may need to do for several bin lists depending on shiftedFlag
            //cout << "addDataPoint " << endl;
            //cout << "dataInitedFlag " << dataInitedFlag << endl;
            if(!dataInitedFlag){
                //cout << "initing data" << endl;
                for(int r=1; r<=nReps; r++){
                    binnedData[r].SetBounds(1,BIN_LIMIT,1,nDims+1);
                    binnedData[r].FillContents(0);
                }
                dataInitedFlag = 1;
            }

            // bin for this dataPoint
            TVector<double> this_bin;
            this_bin.SetBounds(1,nDims);
            this_bin.FillContents(0);

            //cout << "locating bin " << binSizes << endl;
            // for each rep
            for(int r=1; r<=nReps; r++){
                // for each dimension
                this_bin.FillContents(0);
                int valid_dBins=0;
                for(int d=1; d<=nDims; d++){
                    // for each bin
                    for(int b=1; b<=nBins[d]; b++){
                        //cout << bins[r][d][b] << " " << dataPoint[d] << " " << bins[r][d][b]+binSizes[d] << " " ;
                        //cout << (bins[r][d][b] <= dataPoint[d] && dataPoint[d] < bins[r][d][b]+binSizes[d]) << endl;
                        if(b == 1){
                            // just for the last bin check only right margin
                            if(dataPoint[d] < bins[r][d][1]){
                                // found bin for particular d
                                //cout << "dim" << d << " ";
                                valid_dBins += 1;
                                this_bin[d] = b;
                                break;
                            }
                        }
                        else if(b == nBins[d]){
                            // just for the last bin check only left margin
                            if(dataPoint[d] >= bins[r][d][b-1]){
                                // found bin for particular d
                                //cout << "dim" << d << " ";
                                valid_dBins += 1;
                                this_bin[d] = b;
                                break;
                            }
                        }
                        else{
                            //for all other bins, check both margins
                            if(bins[r][d][b-1] <= dataPoint[d] && dataPoint[d] < bins[r][d][b]){
                                // found bin for particular d
                                //cout << "dim" << d << " ";
                                valid_dBins += 1;
                                this_bin[d] = b;
                                break;
                            }
                        }
                    }
                }
                //cout << "valid_dBins=" << valid_dBins << endl;
                if(valid_dBins == nDims){
                    int added = 0;
                    // increment or insert this_bin at binnedData[r][data_len,:]
                    //cout << "nRep = " << r << endl;
                    added = addOrInsertCoords(this_bin,binnedData[r]);
                    if(added==1){
                        dataLen++;
                    }
                    //cout << added << " " << dataLen << " " << binnedData[r].ColumnSize() << endl;
                    //cout << "Before finishing " << r << endl;
                }
            }

            //cout << "Finished adding point" << endl << endl;
            //cout << "Data Length = " << dataLen << " Total Points = " << totalPoints << endl;
        }

        //! Add list of points at a time
        /*     data - TVector with length=number of points, each point being TVector with length=dims
        */
        void addData(TVector<TVector<double> >& data){
            for(int d=1; d<=data.Size(); d++)
                addDataPoint(data[d]);
        }

        /*******************
        * Information tools
        *******************/
        //!Returns entropy of var along dims with varIDs==0
        /*!Example:
        if dims = 4, 4D datapoints will be added, but if only the first 2 dimensions make up the variable of interest, then set
        varIDs[1] = 1; varIDs[2] = 1; varIDs[3] = -1; varIDs[4] = -1\n
        The dims with varID==-1 will be ignored
        */
        double entropy(TVector<int>& vIDs){
            if(vIDs.Size() != nDims){
                cerr << "varIDs argument must be of size = total dimensionality = " << nDims << endl;
                cerr << "Skipping this call" << endl;
                return 0.;
            }

            TVector<int> varIDs;
            normalizeBounds(varIDs, vIDs);

            double entropy = 0.;
            TVector<double> p_x;
            computeIndProbs(p_x,varIDs);

            // iterate over all x values
            for(int xi=1; xi<=p_x.Size(); xi++){
                if(p_x[xi] > 0)
                    entropy -= p_x[xi]*log2(p_x[xi]);
            }
            return entropy;
        }

        //! Return mutual information between vars along dims varIDs==0 and varIDs==1
        /*! Set other varIDs of dims to be ignored to -1
        */
        double mutualInfo(TVector<int>& vIDs){
            if(vIDs.Size() != nDims){
                cerr << "varIDs argument must be of size = total dimensionality = " << nDims << endl;
                cerr << "Skipping this call" << endl;
                return 0.;
            }

            TVector<int> varIDs;
            normalizeBounds(varIDs, vIDs);

            // computer probabilities given the var IDs
            TMatrix<double> p_xy;
            computeJointProbs(p_xy,varIDs);

            //cout << "From mutualInfo"<< endl << p_xy << endl;

            double mi = 0.0;
            // parse through each unique data point
            for (int i = 1; i <= p_xy.ColumnSize(); i++)
            {
                mi += p_xy[i][3]*log2(p_xy[i][3]/(p_xy[i][1]*p_xy[i][2]));
                //cout << "from mi = " << p_xy[i][3]*log2(p_xy[i][3]/(p_xy[i][1]*p_xy[i][2])) << endl;
            }
            return mi;
        }

        #ifndef DOXYGEN_SHOULD_SKIP_THIS
        void specificInfo(TVector<double>& si, TVector<int>& varIDs){
            // specific info for var values identified by varIDs==0, in si

            // ID 0 is the one we want specific information about
            TVector<TVector<TVector<double> > > px;
            //cout << "in specific info " << endl;
            computeSpecProbs(px, varIDs);
            //cout << " Back in spec info " << endl;

            si.SetBounds(1,px.Size());

            for (int x = 1; x <= px.Size(); x++)
            {
                si[x] = 0.0;
                for (int y = 1; y <= px[x][2].Size(); y++)
                {
                    si[x] += px[x][3][y] * log2(px[x][3][y] / (px[x][1][1] * px[x][2][y]));
                    //cout << px[x][1][1] << " " << px[x][2][y] << " " << px[x][3][y] << " " << px[x][3][y] * log2( px[x][3][y] / (px[x][1][1] * px[x][2][y])) << endl;
                }
                //si[x]=si[x]/px[x][1][1]; //XXX not really specific information
            }
        }
        #endif /* DOXYGEN_SHOULD_SKIP_THIS */

        //! Returns redundant information about varIDs==0, in varIDs==1 and varIDs==2
        /*! Set other varIDs of dims to be ignored to -1
        */
        double redundantInfo(TVector<int>& vIDs){
            if(vIDs.Size() != nDims){
                cerr << "varIDs argument must be of size = total dimensionality = " << nDims << endl;
                cerr << "Skipping this call" << endl;
                return 0.;
            }

            TVector<int> varIDs;
            normalizeBounds(varIDs, vIDs);

            TVector<double> siX1;
            TVector<double> siX2;
            TVector<double> p_y;

            TVector<int> varIDsX1, varIDsX2, varIDsY;
            varIDsX1.SetBounds(1,varIDs.Size());
            varIDsX2.SetBounds(1,varIDs.Size());
            varIDsY.SetBounds(1,varIDs.Size());

            for(int d=1; d<=varIDs.Size(); d++){
                // spec Y
                if(varIDs[d]==0) {
                    varIDsY[d] = 0;
                    varIDsX1[d] = 0;
                    varIDsX2[d] = 0;
                }
                // in X1
                if(varIDs[d]==1) {
                    varIDsY[d] = -1;
                    varIDsX1[d] = 1;
                    varIDsX2[d] = -1;
                }
                // in X2
                if(varIDs[d]==2) {
                    varIDsY[d] = -1;
                    varIDsX1[d] = -1;
                    varIDsX2[d] = 1;
                }
            }
            //cout << "varIDs " << varIDsX1 << "--" << varIDsX2 << endl;

            computeIndProbs(p_y, varIDsY);
            specificInfo(siX1,varIDsX1);
            specificInfo(siX2,varIDsX2);

            double ri = 0.0;

            //
            for (int l = 1; l <= siX1.Size(); l++)
            {
                ri += (siX1[l]<siX2[l]?siX1[l]:siX2[l]);
            }
            return ri;
        }

        //! Returns amount of unique information about varIDs==0, from varIDs==1 and not from varIDs==2
        /*! Set other varIDs of dims to be ignored to -1
        */
        double uniqueInfo(TVector<int>& vIDs){
            if(vIDs.Size() != nDims){
                cerr << "varIDs argument must be of size = total dimensionality = " << nDims << endl;
                cerr << "Skipping this call" << endl;
                return 0.;
            }

            TVector<int> varIDs;
            normalizeBounds(varIDs, vIDs);

            TVector<int> varIDsX1;
            varIDsX1.SetBounds(1,varIDs.Size());

            for(int d=1; d<=varIDs.Size(); d++){
                // spec Y
                if(varIDs[d]==0) {
                    varIDsX1[d] = 0;
                }
                // in X1
                if(varIDs[d]==1) {
                    varIDsX1[d] = 1;
                }
                // in X2
                if(varIDs[d]==2) {
                    varIDsX1[d] = -1;
                }
            }

            double infoX1 = mutualInfo(varIDsX1);
            double redun = redundantInfo(varIDs);
            //cout << "From unique info" << endl;
            //cout << "Total info from " << varIDsX1 << " = " << infoX1 << endl;
            //cout << "Redun info from " << varIDs << " = " << redun << endl;

            return infoX1 - redun;

        }

        //! Returns amount of synergistic information about varIDs==0, in varIDs==1 and varIDs==2
        /*! Set other varIDs of dims to be ignored to -1
        */
        double synergy(TVector<int>& vIDs){
            if(vIDs.Size() != nDims){
                cerr << "varIDs argument must be of size = total dimensionality = " << nDims << endl;
                cerr << "Skipping this call" << endl;
                return 0.;
            }

            TVector<int> varIDs;
            normalizeBounds(varIDs, vIDs);

            TVector<int> varIDsX1, varIDsX2, varCommon;
            varIDsX1.SetBounds(1,varIDs.Size());
            varIDsX2.SetBounds(1,varIDs.Size());
            varCommon.SetBounds(1,varIDs.Size());

            for(int d=1; d<=varIDs.Size(); d++){
                // spec Y
                if(varIDs[d]==0) {
                    varIDsX1[d] = 0;
                    varIDsX2[d] = 0;
                    varCommon[d] = 0;
                }
                // in X1
                if(varIDs[d]==1) {
                    varIDsX1[d] = 1;
                    varIDsX2[d] = -1;
                    varCommon[d] = 1;
                }
                // in X2
                if(varIDs[d]==2) {
                    varIDsX1[d] = -1;
                    varIDsX2[d] = 1;
                    varCommon[d] = 1;
                }
            }

            double mi = mutualInfo(varCommon);
            double infoX1 = mutualInfo(varIDsX1);
            double infoX2 = mutualInfo(varIDsX2);
            double redun = redundantInfo(varIDs);

            double synergy = mi - infoX1 - infoX2 + redun;
            //cout << "mutualInfo = " << mi << endl;
            //cout << "uniqueInfoX1 = " << infoX1 - redun << endl;
            //cout << "uniqueInfoX2 = " << infoX2 - redun << endl;
            //cout << "redundancy = " << redun << endl;
            //cout << "synergy = " << synergy << endl;

            return synergy;
        }


        //! Estimates complete info decomposition in infos, returns
        /*!     total mutual information about varIDs==0, from varIDs==1 and varIDs==2\n
        *     unique info about varIDs==0 in varIDs==1\n
        *     unique info about varIDs==0 in varIDs==2\n
        *     redundant info about varIDs==0, from varIDs==1 and varIDs==2\n
        *     synergistic info about varIDs==0, from varIDs==1 and varIDs==2\n
        * Set other varIDs of dims to be ignored to -1
        */
        void pid(TVector<int>& vIDs, TVector<double>& infos){
            if(vIDs.Size() != nDims){
                cerr << "varIDs argument must be of size = total dimensionality = " << nDims << endl;
                cerr << "Skipping this call" << endl;
                return;
            }

            TVector<int> varIDs;
            normalizeBounds(varIDs, vIDs);

            TVector<int> varIDsX1, varIDsX2, varCommon;
            varIDsX1.SetBounds(1,varIDs.Size());
            varIDsX2.SetBounds(1,varIDs.Size());
            varCommon.SetBounds(1,varIDs.Size());

            for(int d=1; d<=varIDs.Size(); d++){
                // spec Y
                if(varIDs[d]==0) {
                    varIDsX1[d] = 0;
                    varIDsX2[d] = 0;
                    varCommon[d] = 1;
                }
                // in X1
                if(varIDs[d]==1) {
                    varIDsX1[d] = 1;
                    varIDsX2[d] = -1;
                    varCommon[d] = 0;
                }
                // in X2
                if(varIDs[d]==2) {
                    varIDsX1[d] = -1;
                    varIDsX2[d] = 1;
                    varCommon[d] = 0;
                }
            }

            double mi = mutualInfo(varCommon);
            double infoX1 = mutualInfo(varIDsX1);
            double infoX2 = mutualInfo(varIDsX2);
            double redun = redundantInfo(varIDs);

            double synergy = mi - infoX1 - infoX2 + redun; // because redun is subtracted twice

            infos.SetBounds(1,5);
            infos[1] = mi;
            infos[2] = infoX1 - redun; // unique X1
            infos[3] = infoX2 - redun; // unique X2
            infos[4] = redun;
            infos[5] = synergy;
        }

        #ifndef DOXYGEN_SHOULD_SKIP_THIS
        double transfer_entropy_1_delay(TVector<int> varIDs){
            // one delay transfer entropy from varIDs==0 to varIDs==1
            double te = 0.;

            return te;
        }
        #endif /*  DOXYGEN_SHOULD_SKIP_THIS */

        /*******************
        * Utils
        *******************/
        //! Clear all data and start over - create another object instead
        void clearAllData(){
            bins.SetSize(0);
            binnedData.SetSize(0);
            avgBinnedData.SetSize(0,0);
        }

        #ifndef DOXYGEN_SHOULD_SKIP_THIS
        void normalizeBounds(TVector<double>& normVec, TVector<double>& vec){
            normVec.SetBounds(1,vec.Size());
            int d1=1;
            for(int d=vec.LowerBound();d<=vec.UpperBound();d++){
                normVec[d1] = vec[d];
                d1+=1;
            }
        }
        void normalizeBounds(TVector<int>& normVec, TVector<int>& vec){
            normVec.SetBounds(1,vec.Size());
            int d1=1;
            for(int d=vec.LowerBound();d<=vec.UpperBound();d++){
                normVec[d1] = vec[d];
                d1+=1;
            }
        }

        int addOrInsertCoords(TVector<double>& coordinates, TMatrix<double>& intoMatrix){
            // given bin indices (i.e. bin index along each dim),
            // if bin is already in the list populated bins i.e. in intoMatrix
            //     add 1 to count of number of points in that bin
            // else
            //     insert this bin as a new entry to list with number of points = 1

            int breakFlag, foundFlag, added=0;
            //cout << "in updateBinnedData " << intoMatrix.ColumnSize() << endl;

            int dims = intoMatrix.RowSize()-1;
            int rowLim = intoMatrix.ColumnSize();
            // check for bins because that might be less likely
            foundFlag = 0;
            for(int l=1; l<=intoMatrix.ColumnSize(); l++){
                breakFlag = 0;
                //cout << "\t l=" << l << " intoMatrix[l]=" << intoMatrix[l][1] << " " <<  intoMatrix[l][2] << " coords=" << coordinates << endl;
                // inserting coordinates - didn't find
                if(intoMatrix[l][1] == 0){
                    //cout << "inserting coordinates - didn't find - " << coordinates << endl;
                    for(int d=1; d<=dims; d++){
                        intoMatrix[l][d] = coordinates[d];
                    }
                    intoMatrix[l][dims+1] = 1;
                    foundFlag = 1;
                    added = 1;
                    //cout << "inserting at " << l << endl;
                    return 1; // return added
                }
                else{
                    breakFlag = 0;
                    //cout << "\t" << intoMatrix[l] << ": " << coordinates << endl;
                    // finding matching coordinate
                    for(int d=1; d<=dims; d++){
                        //cout << intoMatrix[l][d] << " " << coordinates[d] << " " << (intoMatrix[l][d] == coordinates[d]) << endl;
                        if(intoMatrix[l][d] == coordinates[d]){
                            breakFlag += 1;
                        }
                        else{
                            break;
                        }
                    }
                    if(breakFlag==dims){
                        //cout << "match found - increment coordinate" << endl;
                        intoMatrix[l][dims+1] += 1;
                        foundFlag = 1;
                        //cout << "incrementing at " << l << endl;
                        return 0; // return added
                    }
                }
            }

            //if(foundFlag==0){
            // ran out of space to add new entry - expand bin size
            //cerr << "********************************** BIN_LIMIT REACHED **********************************" << endl;
            //exit(0);
            int l = rowLim+1;
            TMatrix<double> _intoMatrix;
            _intoMatrix.SetBounds(1,rowLim,1,dims+1);
            for(int i=1;i<=rowLim;i++){
                for(int d=1; d<=dims+1; d++){
                    _intoMatrix[i][d] = intoMatrix[i][d];
                }
            }
            //cout << "expanding BIN_LIMIT" << endl;
            intoMatrix.SetBounds(1,int(rowLim*1.5),1,dims+1);
            intoMatrix.FillContents(0.);
            for(int i=1;i<=rowLim;i++){
                for(int d=1; d<=dims+1; d++){
                    intoMatrix[i][d] = _intoMatrix[i][d];
                }
            }

            for(int d=1; d<=dims; d++){
                intoMatrix[l][d] = coordinates[d];
            }
            intoMatrix[l][dims+1] = 1;
            foundFlag = 1;
            added = 1;
            //cout << "Expanded intoMatric to - " << intoMatrix.ColumnSize() << endl;
            //cout << "binned data is now - " << binnedData[1].ColumnSize() << endl;
            //cout << binnedData[1] << endl;
            //}
            //else{
                //cout << "found/inserted entry for " << coordinates << endl;
            //}
            return added;

        }

        int indexOf(TMatrix<double>& inWhat, TVector<double>& pattern, TVector<int>& atInds){
            // if a specific pattern (pattern) exists in a matrix (inWhat) at specific colukmns (atInds)
            //     return its row number
            // else
            //     return -1

            for(int l=1; l<=inWhat.ColumnSize(); l++){
                int matchCount = 0;
                // for each value in pattern
                for(int p=1; p<=pattern.Size(); p++){
                    if(inWhat[l][atInds[p]]!=pattern[p]){
                        break;
                    }
                    matchCount++;
                }
                if(matchCount == pattern.Size()){
                    // found pattern
                    return l;
                }
            }
            return -1;
        }

        double fetchTotalValue(TMatrix<double>& from, TVector<double>& pattern, TVector<int>& atInds, int index){
            // matches pattern in rows of from at specified atInds columns, and returns the sum of index columns' value of matching row
            // returns 0 if no match found
            double totalValue = 0.;

            //cout << "from.RowSize() " << from.ColumnSize() << " " << pattern.Size() << " ";
            for(int l=1; l<=from.ColumnSize(); l++){
                int matchCount = 0;
                // for each value in pattern
                for(int p=1; p<=pattern.Size(); p++){
                    if(from[l][atInds[p]]!=pattern[p]){
                        break;
                    }
                    matchCount++;
                }
                if(matchCount == pattern.Size()){
                    // found pattern
                    totalValue += from[l][index];
                }
            }

            return totalValue;
        }

        void getXYInds(TVector<int>& xInds, TVector<int>& yInds, TVector<int>& xyInds, TVector<int>& xyDims, TVector<int>& varIDs){
            // given varIDs and references to other lists,
            // returns
            //     xInds: indices where varIDs == 0
            //     yInds: indices where varIDs == 1
            //     xyInds: indices where varIDs == 0 || varIDs == 1
            //     xyDims: dimensionality of x and y dimensions

            xyDims.SetBounds(1,2);
            // Vectors with indices for x and y
            int xDim=0,yDim=0;
            for(int d=1; d<=nDims; d++){
                if(varIDs[d] == 0){
                    xDim++; // xInds.append(d)
                }
                else if(varIDs[d] == 1){
                    yDim++;
                }
            }
            xyDims[1] = xDim;
            xyDims[2] = yDim;
            xInds.SetBounds(1,xDim);
            if(yDim>0){
                yInds.SetBounds(1,yDim);
            }
            xyInds.SetBounds(1,xDim+yDim);

            int xi=1,yi=1,xyi=1;
            for(int d=1; d<=nDims; d++){
                if(varIDs[d] == 0){
                    xInds[xi] = d;xi++;
                    xyInds[xyi] = d; xyi++;
                }
                if(varIDs[d] == 1 && yDim>0){
                    yInds[yi] = d;yi++;
                    xyInds[xyi] = d; xyi++;
                }
            }
        }

        void collapseBinnedData(){
            // After adding all points, before using any infotheory tools,
            // estimate average shifted bin counts here and
            // set dataReadyFlag

            // average across all binnings
            TMatrix<double> _avgBinnedData;
            _avgBinnedData.SetBounds(1,dataLen,1,nDims+1);

            TVector<double> this_bin;
            this_bin.SetBounds(1,nDims);

            TVector<int> atInds;
            atInds.SetBounds(1,nDims);

            int avgLen = 1;
            if(nReps>1){
                for(int r=1; r<=nReps; r++){
                    for(int l=1; l<=binnedData[r].ColumnSize(); l++){
                        if(binnedData[r][l][1] > 0){
                            //cout << "looping " << l << endl;
                            for(int d=1; d<=nDims; d++){
                                this_bin[d] = binnedData[r][l][d];
                                atInds[d] = d;
                            }
                            int binExist = indexOf(_avgBinnedData,this_bin,atInds);
                            //cout << !binExist << " [" << this_bin << "] ";
                            if(binExist == -1){
                                // for each dimension
                                for(int d=1; d<=nDims; d++){
                                    //cout << binnedData[r][l][d] << " ";
                                    _avgBinnedData[avgLen][d] = binnedData[r][l][d];
                                }
                                _avgBinnedData[avgLen][nDims+1] = 0;
                                for(int r=1; r<=nReps; r++){
                                    double counts = fetchTotalValue(binnedData[r],this_bin,atInds,nDims+1);
                                    _avgBinnedData[avgLen][nDims+1] += counts;
                                    //cout << " (" << counts << ") ";
                                }
                                _avgBinnedData[avgLen][nDims+1] /= nReps;
                                //cout << _avgBinnedData[avgLen][nDims+1];
                                totalAvgPoints += _avgBinnedData[avgLen][nDims+1];
                                avgLen++;
                            }
                        }
                    }
                }
                avgLen--;// removing the last unnecessary ++
                dataLen = avgLen;
            }
            else{
                //cout << "nReps else part - dataLen = " << dataLen << " AvgLEn = " << avgLen << endl;
                avgLen = dataLen;
                //cout << "nReps else part - dataLen = " << dataLen << " AvgLEn = " << avgLen << endl;
                //cout << "_avgBinnedData: " << _avgBinnedData.ColumnSize() << " " << _avgBinnedData.RowSize() << endl;
                //cout << "binnedData: " << binnedData[1].ColumnSize() << " " << binnedData[1].RowSize() << endl;
                for(int l=1;l<=dataLen;l++){
                    for(int d=1; d<=nDims+1; d++){
                        _avgBinnedData[l][d] = binnedData[1][l][d];
                    }
                    totalAvgPoints += binnedData[1][l][nDims+1];
                }
                //cout << "nReps else part - Done" << endl;
            }

            avgBinnedData.SetBounds(1,dataLen,1,nDims+1);
            //cout << "Done creating _avgBinnedData " << avgLen << endl;
            for(int l=1;l<=dataLen;l++){
                for(int d=1; d<=nDims+1; d++){
                    //cout << l << " " << d << " ";
                    //cout << avgBinnedData[l][d] << " " << _avgBinnedData[l][d] << endl;
                    avgBinnedData[l][d] = _avgBinnedData[l][d];
                }
            }
            //cout << "end of collapse " << avgBinnedData.ColumnSize() << " " << avgBinnedData.RowSize() << endl;
            //cout << "from collapse " << endl << avgBinnedData << endl;


            // set flag for data ready and delete binnedData
            dataReadyFlag = 1;
            binnedData.SetSize(0); // XXX unable to delete
            //cout << "Done Collapsing data" << endl;
        }
        #endif /* DOXYGEN_SHOULD_SKIP_THIS */


        /*******************
        * Computing probs
        *******************/
        #ifndef DOXYGEN_SHOULD_SKIP_THIS
        void computeIndProbs(TVector<double>& p_x, TVector<int>& varIDs){
            // compute individual probabilties for all data dimensions have varIDs==0, in p_x

            if(dataReadyFlag==0){
                collapseBinnedData();
            }

            TVector<int> xInds, yInds, xyDims, xyInds;
            getXYInds(xInds,yInds,xyInds,xyDims,varIDs);
            int xDim = xyDims[1];

            TVector<double> xpattern;
            xpattern.SetBounds(1,xDim);

            int uniqueXCounts=1,added;
            TVector<double> _p_x;
            _p_x.SetBounds(1,dataLen);
            TMatrix<double> trackerVar;
            trackerVar.SetBounds(1,dataLen,1,xDim+1);
            trackerVar.FillContents(0.);

            for(int l=1; l<=dataLen; l++){
                // construct pattern for x
                for(int xi=1; xi<=xDim; xi++){
                    xpattern[xi] = avgBinnedData[l][xInds[xi]];
                }
                //cout << xpattern << " ";
                // see if we have already seen this pattern
                added = addOrInsertCoords(xpattern,trackerVar);
                if(added==1){
                    //cout << "is new" << endl;
                    // new x pattern
                    _p_x[uniqueXCounts] = fetchTotalValue(avgBinnedData,xpattern,xInds,nDims+1)/totalAvgPoints;
                    uniqueXCounts++;
                }
                //else{
                //    cout << "is old" << endl;
                //}
            }

            uniqueXCounts--;
            // write into actual TVec
            p_x.SetBounds(1,uniqueXCounts);
            for(int xi=1; xi<=uniqueXCounts; xi++){
                p_x[xi] = _p_x[xi];
            }
            //cout << "p_x " << endl << p_x << endl;
        }

        void computeJointProbs(TMatrix<double>& p_xy, TVector<int>& varIDs){
            // Compute joint probabilties for data dims given by varIDs==0 and varIDs==1, in p_xy

            if(dataReadyFlag==0){
                collapseBinnedData();
            }
            //cout << "from computeJointProbs " << endl << avgBinnedData << endl;
            //cout << "Totals = " << dataLen << " " << totalAvgPoints << endl;

            TVector<int> xInds, yInds, xyDims, xyInds;
            getXYInds(xInds,yInds,xyInds,xyDims,varIDs);
            int xDim = xyDims[1];
            int yDim = xyDims[2];

            //cout << "XYInds " << xInds << "==" << yInds << "==" << xyInds << endl;
            TVector<double> xypattern;
            xypattern.SetBounds(1,xDim+yDim);
            TVector<double> xpattern;
            xpattern.SetBounds(1,xDim);
            TVector<double> ypattern;
            ypattern.SetBounds(1,yDim);

            int uniqueXYcounts=1,added;
            TMatrix<double> _p_xy;
            _p_xy.SetBounds(1,dataLen,1,3);
            TMatrix<double> trackerVar;
            trackerVar.SetBounds(1,dataLen,1,xDim+yDim+1);
            trackerVar.FillContents(0.);
            //cout << "Total points = " << totalPoints << endl;
            //cout << "Total Average points = " << totalAvgPoints << endl;
            // go through whole list and compute the probs
            for(int l=1; l<=avgBinnedData.ColumnSize(); l++){
                //for(int d=1; d<=nDims+1; d++)
                    //cout << avgBinnedData[l][d] << " ";
                // construct pattern for x
                int xyi=1;
                for(int i=1; i<=varIDs.Size(); i++){
                    if(varIDs[i]==0 || varIDs[i]==1){
                        xypattern[xyi] = avgBinnedData[l][i];
                        xyi++;
                    }
                }
                //cout << "xypattern = " << xypattern << endl;
                // will add this pattern to trackerVar if it already doesnt exist
                added = addOrInsertCoords(xypattern,trackerVar);
                if(added==1){
                    // then we haven't looked at this combination xbin and ybin
                    // so insert it into _p_xy
                    _p_xy[uniqueXYcounts][3] = fetchTotalValue(avgBinnedData,xypattern,xyInds,nDims+1)/totalAvgPoints;

                    // construct pattern for x
                    for(int xi=1; xi<=xDim; xi++){
                        xpattern[xi] = avgBinnedData[l][xInds[xi]];
                    }
                    _p_xy[uniqueXYcounts][1] = fetchTotalValue(avgBinnedData,xpattern,xInds,nDims+1)/totalAvgPoints;

                    // construct pattern for y
                    for(int yi=1; yi<=yDim; yi++){
                        ypattern[yi] = avgBinnedData[l][yInds[yi]];
                    }
                    _p_xy[uniqueXYcounts][2] = fetchTotalValue(avgBinnedData,ypattern,yInds,nDims+1)/totalAvgPoints;

                    uniqueXYcounts++;
                }
                //cout << _p_xy[l][1] << " " << _p_xy[l][2] << " " << _p_xy[l][3] << endl;
            }
            //cout << "trackerVar..." << endl << trackerVar << endl;

            uniqueXYcounts--;
            p_xy.SetBounds(1,uniqueXYcounts,1,3);
            for(int l=1; l<=uniqueXYcounts; l++){
                for(int d=1; d<=3; d++)
                    p_xy[l][d] = _p_xy[l][d];
            }

            //cout << "Done" << endl << p_xy <<endl;
        }

        void computeSpecProbs(TVector<TVector<TVector<double> > >& p_x, TVector<int>& varIDs){
            if(dataReadyFlag==0){
                collapseBinnedData();
            }
            // p_x :TVector: reference to object to populate and return
            // varIDs :TVector: identifiers for dims of data
            // returns matrix with three columns
            //    p(x) :double: for each value of x for which specific prob is computed
            //    p(y) :TVector: for all y, under this value of x, its p(y), NOT p(y\x)
            //    p(x,y) :TVector: for each X=x, and all y, this is p(X=x,y)

            //cout << "from computeSpecProbs " << endl << avgBinnedData << endl;

            //cout << "in compute probs - " << dataReadyFlag << endl;
            TVector<TVector<TVector<double> > > _p_x;
            _p_x.SetBounds(1,dataLen);
            for(int l=1; l<=dataLen; l++){
                _p_x[l].SetBounds(1,3);
                _p_x[l][1].SetBounds(1,1);
                _p_x[l][2].SetBounds(1,dataLen);
                _p_x[l][3].SetBounds(1,dataLen);
                _p_x[l][1].FillContents(0.);
                _p_x[l][2].FillContents(0.);
                _p_x[l][3].FillContents(0.);;
            }

            TVector<int> xInds, yInds, xyInds, xyDims;
            getXYInds(xInds,yInds,xyInds,xyDims,varIDs);
            int xDim = xyDims[1];
            int yDim = xyDims[2];
            //cout << "XYInds " << xInds << "==" << yInds << "==" << xyInds << endl;

            int uniqueXcounts = 1;
            int added, xyAdded;

            TMatrix<double> trackerVar;
            trackerVar.SetBounds(1,dataLen,1,xDim+1);
            trackerVar.FillContents(0.);

            TMatrix<double> xytrackerVar;
            xytrackerVar.SetBounds(1,dataLen,1,xDim+yDim+1);
            xytrackerVar.FillContents(0.);

            TVector<int> uniqueXYcounts;
            uniqueXYcounts.SetBounds(1,dataLen);
            uniqueXYcounts.FillContents(2.); // since it will only be used from idnex of 2 onwards

            TVector<double> this_xbin,this_ybin,this_xybin;
            TVector<int> trackDim;
            this_xbin.SetBounds(1,xDim);
            trackDim.SetBounds(1,xDim);
            this_ybin.SetBounds(1,yDim);
            this_xybin.SetBounds(1,xDim+yDim);

            //cout << "dataLen = " << dataLen << endl;

            for(int l=1; l<=dataLen; l++){
                //cout << "********************** " << l << endl;
                // spec x
                for(int xi=1; xi<=xDim; xi++){
                    this_xbin[xi] = avgBinnedData[l][xInds[xi]];
                    trackDim[xi] = xi;
                }
                //cout << this_xbin << endl;

                for(int yi=1; yi<=yDim; yi++){
                    this_ybin[yi] = avgBinnedData[l][yInds[yi]];
                }

                int index=1;
                for(int i=1; i<=varIDs.Size(); i++){
                    if(varIDs[i]==0 || varIDs[i]==1){
                        this_xybin[index] = avgBinnedData[l][i];
                        index++;
                    }
                }

                //cout << "Sizes - " << this_xbin.Size() << " " << trackerVar.RowSize() << endl;

                // these x coordinates are inserted or added into trackerVar
                added = addOrInsertCoords(this_xbin,trackerVar);
                //cout << "added = " << added << " unqCounts = " << uniqueXcounts << endl;
                if(added==1){
                    //cout << "new xbin " << this_xbin << endl;
                    // then this is the first occurence of this bin
                    // so add it and add the corresponding y
                    ///_p_x[uniqueXcounts].SetBounds(1,dataLen);
                    // prob of x
                    //_p_x[uniqueXcounts][1].SetBounds(1,1);
                    _p_x[uniqueXcounts][1][1] = fetchTotalValue(avgBinnedData,this_xbin,xInds,nDims+1)/totalAvgPoints;
                    //cout << "added px " << endl;

                    //_p_x[uniqueXcounts][2].SetBounds(1,dataLen);
                    _p_x[uniqueXcounts][2][1] = fetchTotalValue(avgBinnedData,this_ybin,yInds,nDims+1)/totalAvgPoints;
                    //cout << "added py " << endl;

                    //_p_x[uniqueXcounts][3].SetBounds(1,dataLen);
                    _p_x[uniqueXcounts][3][1] = fetchTotalValue(avgBinnedData,this_xybin,xyInds,nDims+1)/totalAvgPoints;
                    //cout << "added pxy " << endl;

                    xyAdded = addOrInsertCoords(this_xybin,xytrackerVar);
                    //cout << "xytrackerVar" << endl << xytrackerVar << endl;
                    //cout << "*************" << endl;
                    uniqueXcounts++;
                }
                else{
                    //cout << "existing xbin " << this_xybin << " ";
                    //cout << this_xbin << endl;
                    //cout << trackerVar << endl;
                    // this bin has alrady occured before
                    // find index of where it was
                    xyAdded = addOrInsertCoords(this_xybin,xytrackerVar);
                    if(xyAdded==1){
                        int ind = indexOf(trackerVar,this_xbin,trackDim);
                        // get its py index
                        //int pyInd = trackerVar[ind][xDim+1];
                        //cout << "and also new xybin to be inserted at " << uniqueXYcounts[ind] << " of " << ind << endl;
                        //cout << ind << " " << pyInd << " " << _p_x.ColumnSize() << " " << _p_x[ind][2].Size() << " " << dataLen << endl;
                        _p_x[ind][2][uniqueXYcounts[ind]] = fetchTotalValue(avgBinnedData,this_ybin,yInds,nDims+1)/totalAvgPoints;
                        _p_x[ind][3][uniqueXYcounts[ind]] = fetchTotalValue(avgBinnedData,this_xybin,xyInds,nDims+1)/totalAvgPoints;
                        uniqueXYcounts[ind]++;
                    }
                    else{
                        //cout << endl;
                    }
                    //cout << "xytrackerVar" << endl << xytrackerVar << endl;
                    //cout << "*************" << endl;
                    //trackerVar[ind][xDim+1]++; // XXX check this
                }
                //cout << "********************** " << l << endl << _p_x << endl << "********************** " << endl;
            }
            uniqueXcounts--;

            // could now shorten all arrays - p_x, p_x[i][2] and p_x[i][3]
            p_x.SetBounds(1,uniqueXcounts);
            //cout <<  _p_x[uniqueXcounts][1][1] << endl;
            for(int l=1; l<=uniqueXcounts; l++){
                p_x[l].SetBounds(1,3);
                p_x[l][1].SetBounds(1,1);
                p_x[l][1][1] = _p_x[l][1][1];
                //cout << "p_x[" << l << "][1][1] = " << _p_x[l][1][1] <<endl;
                for(int d=2; d<=3; d++){
                    p_x[l][d].SetBounds(1,uniqueXYcounts[l]-1);
                    for(int i=1; i<=uniqueXYcounts[l]-1; i++){
                        p_x[l][d][i] =_p_x[l][d][i];
                    }
                }
            }
        }

        /*******************
        * Write outs
        ******************
        void writeBinnedDataOut(){
            //cout << "in write binned data" << endl;
            //cout << binnedData.Size() << endl;
            //cout << binnedData[1][1][1] << endl;

            ofstream binnedDataFile;
            binnedDataFile.open("test_binnedData.dat");
            for(int r=1; r<=nReps; r++){
                for(int l=1; l<=BIN_LIMIT; l++){
                    if(binnedData[r][l][1] == 0)break;
                    binnedDataFile << r << " ";
                    for(int d=1; d<=nDims+1; d++){
                        binnedDataFile << binnedData[r][l][d] << " ";
                    }
                    binnedDataFile << endl;
                }
                binnedDataFile << endl;
            }
            binnedDataFile.close();
            //cout << "Done writing" << endl;
        }


        void writeOutAvgBinnedData(){
            ofstream avgBinnedDataFile;
            avgBinnedDataFile.open("./avgBinnedData.dat");

            for(int l=1; l<=dataLen; l++){
                for(int d=1; d<=nDims+1; d++){
                    avgBinnedDataFile << avgBinnedData[l][d] << " ";
                }
                avgBinnedDataFile << endl;
            }

            avgBinnedDataFile.close();
        }
        */
        #endif /* DOXYGEN_SHOULD_SKIP_THIS */

};
