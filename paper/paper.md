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

Information theory, was first introduced by Claude Shannon in his seminal paper "A mathematical theory of communication"[@shannon1948mathematical], as a methodology to develop efficient coding and communication of data across noisy channels. Its rise to popularity can be primarily attributed to its ability to be applied in any domain, ranging from Economics to Neuroscience. Information theory enables us to answer questions such as, "how can we quantify the difference in uncertainty in random process versus another?", and "how much does knowing the value of one random variable, reduce uncertainty about another?". Since Shanon's introduction of information theory, there have been several advancements that allows study of information transfer over time and through the interaction of multiple sources of information. They provide a set of tools that enable us to understand the relationships and interactions between arbitrary multivariate random variables.
These advancements enable us to ask more involved questions such as, "what is the amount of information transferred from one random process to another over time?", and "Of these multiple sources, what is thee amount of information that is redundantly transferred from all sources about a target random variable?". These crucial questions enable us to understand the interactions between different components of a complex system, and can ultimately lead to a mechanistic understanding of its operation.

This paper introduces Infotheory, a fully open-source package for information theoretic analyses of discrete and continuous valued multivariate data that can be used in Python or C++ (available at [https://git.io/infot](https://git.io/infot)). This package implements more widely used measures such as entropy and mutual information [@cover2012elements], as well as more involved measures such as Partial Information Decomposition (PID)[@williams2010nonnegative], where interactions between variables in a multivariate system can be studied by decomposing the total information that multiple variables provide about a target variable into its constituent redundant, unique and synergistic components. It has been designed to be easy to use and would be ideal for pedagogical demonstrations of information theory as well as in research. The main highlights of this package include:(a) being written in C++ for efficiency, (b) ease of use via python bindings and compatibility with numpy, (c) an API that allows adding the data once to then be able to perform various analyses across different sub-spaces of the dataset very quickly, (d) use of sparse data structures that work well with high-dimensional data (e) better data distribution using averaged shifted histograms [@scott1985averaged] and (f) user-controllable specification of binning allowing proper estimation of information measures in data that that has a mix of continuous and discrete variables.



# Acknowledgements

VectorMatrix?, NSF funding?, Cog. Sci.?

# References
