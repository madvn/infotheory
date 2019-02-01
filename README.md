<!-- ## Website and docs-->

<!-- https://madvn.github.io/infotheory/ -->

## Introduction

Infotheory, written in C++, is a software package to perform information theoretic analysis, especially on high-dimensional data. While inferring the data distribution from samples, we've utilized sparse representations thus avoiding the catastrophic explosion of bin counts with increased dimensions. Moreover, this package enables better distribution estimation by employing averaged shifted histograms [1].

The following information theoretic quantities can be estimated using this tool as of now and follow this repo for more to come.

1. Entropy [2]
2. Mutual Information [3]
3. Partial Information Decomposition measures [4]
   - Unique Information
   - Redundant Information
   - Synergistic Information

The package can be used in Python or C++. While the C++ headers should function well on all platforms, the python package has currently only been tested on MacOS and Linux.

## Installation

    pip install infotheory

On MacOS, upgrade to MacOS-Mojave and update Xcode. You might have to set these environment variables from your terminal.

    export CXXFLAGS="-mmacosx-version-min=10.9"
    export LDFLAGS="-mmacosx-version-min=10.9"

For C++, simply download [InfoTools.h](https://github.com/madvn/infotheory/blob/master/infotheory/InfoTools.h) and [VectorMatrix.h](https://github.com/madvn/infotheory/blob/master/infotheory/VectorMatrix.h) and include those header files in your code.

## Usage

Using this package in your own code involves three steps.

<p align="center">
<img src="https://github.com/madvn/infotheory/blob/master/demos/usage_icons.png" width="480">
</p>

See [demos](https://github.com/madvn/infotheory/tree/master/demos) and [website](https://madvn.github.io/infotheory/) for sample programs on how to use this package.

See colab demo [here](https://colab.research.google.com/drive/1Pu0QIS7bsx8AjVXRIuAxPdbifkBFToLu)

## Contact

Created by Madhavun Candadai and Eduardo J. Izquierdo. Contact Madhavun at madvncv[at]gmail.com

## References

<ol>
    <li id="scott:1985">Scott, D. W. (1985). Averaged shifted histograms: effective nonparametric density estimators in several dimensions. The Annals of Statistics, 1024-1040.</li>
    <li id="scholarpedia:Shannon_entropy"><a href="http://www.scholarpedia.org/article/Entropy#Shannon_entropy" target="_blank"> http://www.scholarpedia.org/article/Entropy#Shannon_entropy</a></li>
    <li id="scholarpedia:Mutual_information"><a href="http://www.scholarpedia.org/article/Mutual_information" target="_blank"> http://www.scholarpedia.org/article/Mutual_information</a></li>
    <li id="williams:2010">Williams, P. L., & Beer, R. D. (2010). Nonnegative decomposition of multivariate information. arXiv preprint arXiv:1004.2515.</li>
</ol>
