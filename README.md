# Infotheory
[![Build Status](https://travis-ci.org/madvn/infotheory.svg?branch=master)](https://travis-ci.org/madvn/infotheory)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/madvn/infotheory/blob/master/LICENSE)

Website: [http://mcandadai.com/infotheory/](http://mcandadai.com/infotheory/)

## Introduction

Infotheory, written in C++, and usable in Python as well, is a software package to perform information theoretic analysis on multivariate data. This package implements traditional as well as more recent measures that arise from multivariate extensions to information theory, specifically

<ol class="ml-25">
   <li>Entropy <a href="#scholarpedia:Shannon_entropy">[1]</a></li>
   <li>Mutual Information <a href="#scholarpedia:Mutual_information">[2]</a></li>
   <li>Partial Information Decomposition <a href="#williams:2010">[3]</a>
       <ul class="ml-25" style="margin-bottom:0px;">
           <li>Unique Information</li>
           <li>Redundant Information</li>
           <li>Synergistic Information</li>
       </ul></li>
</ol>

The main highlights of this package include:
<ul class="ml-25">
   <li>being written in C++ for efficiency</li>
   <li>ease of use via python bindings and compatibility with numpy</li>
   <li>an API that allows adding the data once to then be able to perform various analyses across different sub-spaces of the dataset very quickly</li>
   <li>use of sparse data structures that work well with high-dimensional data</li>
   <li>user-controllable estimation of data distribution using averaged shifted histograms <a href="#scott:1985">[4]</a></li>
   <li>flexibilty to specify binning allows proper estimation of information measures between continuous and discrete variables</li>
   <li>perform PI-decomposition over 3 (two sources and 1 target) and 4 (three variables and 1 target) variables</li>
</ul>

The package can be used in Python or C++. While the C++ headers should function well on all platforms, the python package has currently been tested on MacOS and Linux.

## Citing

If you use this package, please cite preprint available at: [https://arxiv.org/abs/1907.02339](https://arxiv.org/abs/1907.02339)

Candadai, M., & Izquierdo, E. J. (2019). infotheory: A C++/Python package for multivariate information theoretic analysis. arXiv preprint arXiv:1907.02339.

      @article{candadai2019infotheory,
        title={infotheory: A C++/Python package for multivariate information theoretic analysis},
        author={Candadai, Madhavun and Izquierdo, Eduardo J},
        journal={arXiv preprint arXiv:1907.02339},
        year={2019}
      }

## Installation

    pip install infotheory

On MacOS, upgrade to MacOS-Mojave and update Xcode. You might have to set these environment variables from your terminal.

    export CXXFLAGS="-mmacosx-version-min=10.9"
    export LDFLAGS="-mmacosx-version-min=10.9"

For C++, simply download [InfoTools.h](https://github.com/madvn/infotheory/blob/master/infotheory/InfoTools.h) and [VectorMatrix.h](https://github.com/madvn/infotheory/blob/master/infotheory/VectorMatrix.h) and include those header files in your code.

## Usage

Using this package in your own code involves the following steps.

<p align="center">
<img src="https://github.com/madvn/infotheory/blob/master/demos/usage_icons.png" width="480">
</p>

See [demos](https://github.com/madvn/infotheory/tree/master/demos/python) and [website](http://mcandadai/infotheory/) for sample programs on how to use this package.

## Contact

Created by Madhavun Candadai and Eduardo J. Izquierdo. If you have questions or if you've found a bug, please file an issue or feel free to contact Madhavun at madvncv[at]gmail.com

## Contribution

If you'd like a feature to be added to `infotheory`, please file an issue. Or, better yet, open a pull request. We'll work with you to ensure that all pull requests are in a mergable state.

## References
<ol class="ml-25">
    <li id="scholarpedia:Shannon_entropy"><a href="http://www.scholarpedia.org/article/Entropy#Shannon_entropy" target="_blank"> http://www.scholarpedia.org/article/Entropy#Shannon_entropy</a></li>
    <li id="scholarpedia:Mutual_information"><a href="http://www.scholarpedia.org/article/Mutual_information" target="_blank"> http://www.scholarpedia.org/article/Mutual_information</a></li>
    <li id="williams:2010">Williams, P. L., & Beer, R. D. (2010). Nonnegative decomposition of multivariate information. arXiv preprint arXiv:1004.2515.</li>
    <li id="scott:1985">Scott, D. W. (1985). Averaged shifted histograms: effective nonparametric density estimators in several dimensions. The Annals of Statistics, 1024-1040.</li>
    <li id="timme:2014">Timme, N., Alford, W., Flecker, B., & Beggs, J. M. (2014). Synergy, redundancy, and multivariate information measures: an experimentalist’s perspective. Journal of computational neuroscience, 36(2), 119-140.</li>
</ol>
