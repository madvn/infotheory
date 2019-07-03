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

Information theory, was first introduced by Claude Shannon in his seminal paper "A mathematical theory of communication"[@shannon1948mathematical], as a methodology to develop efficient coding and communication of data across noisy channels. Its rise to popularity can be primarily attributed to its ability to be applied in any domain, ranging from Economics to Neuroscience. Information theory enables us to answer questions such as, "how can we quantify the difference in uncertainty in one random process versus another?", and "how much does knowing the value of one random variable, reduce uncertainty about another?". Since Shanon's introduction of information theory, there have been several advancements that allows study of information transfer over time and through the interaction of multiple sources of information. They provide a set of tools that enable us to understand the relationships and interactions between arbitrary multivariate random variables.
These advancements enable us to ask more involved questions such as, "what is the amount of information transferred from one random process to another over time?", and "Of these multiple sources, what is thee amount of information that is redundantly transferred from all sources about a target random variable?". These crucial questions enable us to understand the interactions between different components of a complex system, and can ultimately lead to a mechanistic understanding of its operation.

This paper introduces Infotheory, a fully open-source package for information theoretic analyses of discrete and continuous valued multivariate data that can be used in Python or C++ (available at [https://git.io/infot](https://git.io/infot)). This package implements more widely used measures such as entropy and mutual information [@cover2012elements], as well as more involved measures such as Partial Information Decomposition (PID)[@williams2010nonnegative], where interactions between variables in a multivariate system can be studied by decomposing the total information that multiple variables provide about a target variable into its constituent redundant, unique and synergistic components. It has been designed to be easy to use and would be ideal for pedagogical demonstrations of information theory as well as in research. The main highlights of this package include:(a) being written in C++ for efficiency, (b) ease of use via python bindings and compatibility with numpy, (c) an API that allows adding the data once to then be able to perform various analyses across different sub-spaces of the dataset very quickly, (d) use of sparse data structures that work well with high-dimensional data (e) better data distribution using averaged shifted histograms [@scott1985averaged], an alternative to the most commonly available kernel methods and (f) user-controllable specification of binning allowing proper estimation of information measures in data that that has a mix of continuous and discrete variables. These features, especially the ability to flexibly work with discrete and continuous data as well as the utilization of average shifted histograms, make our package a valuable augmentation to two existing packages, namely dit [@james2018dit] and IDTxL [@wollstadt12019IDTxl]. More details on how to install and use our package can be found on its [website](http://mcandadai.com/infotheory/).

Mutual information forms the fundamental building block of most advanced information theoretic analyses. Infotheory, our package, implements bivariate mutual information in a way that easily allows expansion to the multivariate case. With regards to multivariate systems, implementing bivariate measures pairwise is insufficient to capture the polyadic interactions between the different variables [@james2017multivariate]. There has been multiple approaches proposed to extend bivariate measures to the multivariate case [@williams2010nonnegative, @griffith2014quantifying, @bertschinger2014quantifying, @james2018unique] and here we follow Partial Information Decomposition (PID) by @williams2010nonnegative. Specifically, for the trivariate case, we implement PID such that upon separating the three variables into a target and two source variables, the total information that the two sources have about the target (bivariate information with sources as one variable and target as the other), can be decomposed into the following non-negative components: information that each source uniquely provides about the target, information that they redundantly provide and the synergistic information that is only available when both sources are known.

In addition to the measures that are directly available from the package, they have been designed such that it can be adapted for more sophisticated use. For instance, the decomposed information atoms can also be combined to measure transfer entropy [@schreiber2000measuring]. When dealing with time-series data, one can restructure the data such that the two sources are past values of two random variables, and the target is a future value of one of them. It has been shown that, the sum of the unique information that a source provides about the target (future value) and the synergistic information from both sources is equal to the amount if information transferred from that source [@williams2011generalized]. Transfer entropy is used quite extensively in neuroscience in order to infer directed functional connections between nodes of a network (nodes can be neurons, brain regions or EEG electrodes) from recorded data [@wibral2014transfer]. Another instance of expanded use of this package can be with regards to measuring information in time. Since these measures are designed agnostic of any data or file format, one can devise different measures by providing different subsets of the data appropriately. With a time-series data, if one were to provide all data over all time-points, then one can measure all these measures as aggregate values over time. On the other hand, providing data points that are only from a specific time point, and repeating the analyses over the entire time course allows the study of information in time. This is crucial in neuroscience where we are interested in understanding the neural basis of ongoing behavior.

Our package, infotheory, provides an easy-to-use efficient and flexible approach to performing such analyses on any dataset. Application areas are theoretically as wide as information theory in general. Any domain that has a multivariate system and aims to study the relationship between them. Pertaining to the field of neuroscience, that we work in, this package can be used to quantify information about the provided stimulus encoded in neurons, or brain regions (any recorded data), to study the dynamics of information over time, infer directed functional connections between the nodes of a network, and study how information recorded from one node of a network about the stimulus may be compared with another node to illuminate the structure of dependencies in information encoding between them, namely unique, redundant and synergistic information encoding. Besides its potential use in research, we hope that this package with its short learning curve can also be used for pedagogical purposes to introduce students to information theory (the website provides a few benchmarks and examples). We also hope to improve upon this release by implementing the other approaches to multivariate information analyses and in the spirit of free and open-source software development welcome anyone interested to contribute.

# Acknowledgements

VectorMatrix?, NSF funding?, Cog. Sci. dept. that gave assistantship to me for developing this?

# References
