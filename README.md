# oviIN-inputs
Studying the sub-connectome induced by the inputs to oviIN. Includes scripts to process the data and produce figures.

get_connectome.py - queries the Hemibrain to obtain a sub-connectome from the inputs and/or outputs of a specified neuron or group of neurons. This function was initially written by Rhessa and modified by Gabrielle. 

format_edgelist.py - formats the sub-connectome in preparation for running modularity on it. This function was contributed by Alex. 

Figure Files:
[piechart.ipynb](oviIN-inputs/piechart.ipynb) - produces both piechart figures using the preprocessed_nodes.csv. 

[comparisons_to_fullHB.ipynb](oviIN-inputs/comparisons_to_fullHB.ipynb) - computes both joint marginals between the whole brain data and oviIN input connectome and jaccard similarity between connectomes. Needs the input of preprocessed_nodes.csv for both oviIN connectome and whole brain connectome.
