---
title: 'Infotheory: A C++/Python package for multivariate information theoretic analysis'
tags:
  - Python
  - C++
  - information theory
  - multivariate data analysis
  - entropy
  - mutual information
  - partial information decomposition
authors:
  - name: Madhavun Candadai
    orcid:
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Eduardo J. Izquierdo
    orcid:
    affiliation: "1, 2"
affiliations:
 - name: Program in Cognitive Science, Indiana University, Bloomington, IN, U.S.A.
   index: 1
 - name: School of Informatics, Computing and Engineering, Indiana University, Bloomington, IN, U.S.A.
   index: 2
date: 03 July 2019
bibliography: paper.bib
---

# Summary

Information theory was first introduced by Claude Shannon in his seminal paper "A mathematical theory of communication" as a methodology to develop efficient coding and communication of data across noisy channels [@shannon1948]. Its rise to popularity can be primarily attributed to its ability to be applied in any domain, ranging from Economics to Neuroscience. Information theory enables us to answer questions such as, how can we quantify the difference in uncertainty in one random process versus another?, and how much does knowing the value of one random variable, reduce uncertainty about another?. Until relatively recent, information theory had been employed to study n-dimensional systems two variables at a time. However, all natural systems are multivariate and a scientific inquiry into their operation requires understanding how these multiple variables interact. In a multivariate system, bivariate measures such as pairwise mutual information alone are insufficient to capture the polyadic interactions between the different variables [@james2017]. There have been multiple approaches proposed to extend bivariate measures to the multivariate case [@williams2010, @griffith2014, @bertschinger2014, @james2018a]. Here we focus on the approach of Partial Information Decomposition (PID) by [@williams2010]. In PID, interactions between variables in a multivariate system can be studied by decomposing the total information that multiple source variables provide about a target variable into its constituent non-negative components. More specifically, in a trivariate case, the three variables can be separated into one target and two source variables. The total information that the two sources have about the target is given by the bivariate mutual information between the concatenated sources as one variable and the target. Using PID, the dependencies between the sources can be studied by decomposing this total information into the following non-negative components: information that each source uniquely provides about the target, information that they redundantly provide and the synergistic information that is only available when both sources are known. Multivariate analysis, such as PID, allows us to ask more detailed questions such as, what is the amount of information that is redundantly transferred from multiple sources about a target random variable?, and what is the amount of information that is transferred from one random process X to another Y over and above Y’s own information from its past?. These crucial questions enable us to understand the interactions between different components of a complex system, thereby leading us towards an understanding of its operation given just the observed data from the system.

This paper introduces ``infotheory``: a package that implements multivariate information theoretic measures for discrete and continuous data. This package implements widely used measures such as entropy and mutual information [@cover2012], as well as more recent measures that arise from multivariate extensions to information theory.
As such, the tool has been designed to be easy to use and is ideal for pedagogical demonstrations of information theory as well as in research.
``infotheory`` is open-source ([https://git.io/infot](https://git.io/infot)) and details on how to install it and use it are available on its [website](http://mcandadai.com/infotheory/).
Here, we highlight six key aspects of its implementation that make our package a valuable addition to any information theoretic analyses toolbox along with two existing packages, namely dit [@james2018b] and IDTxL [@wollstadt12019].
First, the package is written in C++. One of the main challenges of multivariate analysis on a large, complex system is the amount of computations involved. The C++ implementation makes the package efficient.
Second, the package can be used from either C++ or Python. Python wrapping allows for ease of use, as well as compatibility with other powerful open-source libraries such as numpy.
Third, the API allows adding the data only once to then perform various analyses across different sub-spaces of the dataset cheaply.
Fourth, the data structure used to represent the random variables is sparse. This allows the package to work easily with high-dimensional data.
Fifth, the package employs a method called 'averaged shifted histograms' [@scott1985] that can be used to better estimate the distribution of a random variable in the case of continuous data.
Finally, the package includes user-controllable specification of binning. This is essential for estimating distributions on hybrid systems with a mix of continuous and discrete variables.

The functions implementing the above mentioned information theoretic measures have been designed to be flexibly used in alternative ways. For instance, the decomposed information components can be combined to measure transfer entropy [@schreiber2000]. When dealing with time-series data, one can restructure the data such that the two sources are past values of two random variables, and the target is a future value of one of them. It has been shown that the sum of the unique information that a source provides about the target (future value) and the synergistic information from both sources is equal to the amount of information transferred from that source [@williams2011]. Transfer entropy is used extensively in neuroscience to infer directed functional connections between nodes of a network (nodes can be neurons, brain regions or EEG electrodes) from recorded data [@wibral2014]. Another instance of expanded use of this package is to measure changes in information in time. With time-series data, if the user provides all data over all time-points, then they can ask the tool to calculate all the previously discussed measures as aggregate values over time. However, the user can alternatively provide data points that are only from a specific time point, calculate the information theoretic measures for that time point, and then repeat the analyses over the entire time course. Such analysis reveals how information in the variables of the system change dynamically during the course of its operation [@izquierdo2015, @beer2015]. Both extensions are easily accessible by reusing the existing mutual information and PID functions in the package and providing different subsets of the data accordingly.

Altogether, ``infotheory`` provides an easy-to-use and flexible tool to performing information theoretic analyses on any multivariate dataset consisting of discrete or continuous data. Application areas are, in principle, as wide as that of information theory's - any domain that has a multivariate system and aims to study how the different components interact. We are particularly encouraged by the potential applications in neuroscience at all scales ranging from individual neurons to brain regions to integrated brain-body-environment systems. In our group, we are currently using this package to understand the flow of information in neural circuits capable of producing behavior. This tool allows us to easily analyze how different neurons of a circuit or regions in the brain are encoding information about the sensory stimulus it is receiving, the actions it is producing, or indeed about other neurons/regions within the system itself. We are using multivariate measures to analyze how different nodes in the circuit encode information uniquely, redundantly, and synergistically about the source. We are using the tool to study the dynamics of the neural circuit over time during behavior. We are also using it to infer directed functional connections between the nodes of the network. Besides its use in research, we are using this package for pedagogical purposes to introduce students to information theory. As such, we have provided a number of benchmarks and examples in the [website](http://mcandadai.com/infotheory/). We also hope to continue to extend the package in the future by, for example, implementing additional approaches to multivariate information analyses, providing GPU-support. Finally, in the spirit of free and open-source software development, we also welcome contributions from others.

# Acknowledgements

The work in this paper was supported in part by NSF grant No. IIS-1524647.
VectorMatrix? Cog. Sci. dept. that gave assistantship to me for developing this?

# References
