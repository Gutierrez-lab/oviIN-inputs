# oviIN-inputs
**Studying the sub-connectome induced by the inputs to oviIN. Includes scripts to process the data and produce figures.**

[get_connectome.py](get_connectome.py) - queries the Hemibrain to obtain a sub-connectome from the inputs and/or outputs of a specified neuron or group of neurons. This function was initially written by Rhessa and modified by Gabrielle. 

[format_edgelist.py](gcm_pipeline/format_edgelist.py) - formats the sub-connectome in preparation for running modularity on it. This function was contributed by Alex. 

Figure Files:

[piechart.ipynb](piechart.ipynb) - produces both piechart figures using the preprocessed_nodes.csv. 

[comparisons_to_fullHB.ipynb](comparisons_to_fullHB.ipynb) - computes both joint marginals between the whole brain data and oviIN input connectome and jaccard similarity between connectomes. Needs the input of preprocessed_nodes.csv for both oviIN connectome and whole brain connectome.

[mesoscale_connectivity.ipynb](mesoscale_connectivity.ipynb) - produces analyses about the top 33 inputs to the oviINr based on synaptic weight. Also contains code for the skeleton plots with synaptic connectivity plotted on the arbor and colored by module id that the input neuron is sorted into.

[oviposition_circuit.ipynb](oviposition_circuit.ipynb) - produces plots of synapse counts in oviposition circuit for figure 1. Needs to be cleaned up. File can be renamed after editing.

[hub_bespoke.ipynb](hub_bespoke.ipynb) - produces the primacy plots and addition statistics about the inputs of the oviIN. Both figures pull data from neuprint and the second figure requires modularity data.

[ovi_specs_rankings.ipynb](ovi_specs_rankings.ipynb) - produces plots of rankings within the full Hemibrain for figure 2. Also needs to be cleaned up and better organized. File can be renamed after editing.

[cluster_deep_dive.ipynb](cluster_deep_dive.ipynb) - produces the wireframe plot with module-color-coded synaptic sites from figure 4C. There is also a lot of extra stuff that needs to be cleared out and Rhessa's code for creating figures 4A&B needs to be incorporated. File should be renamed when that happens. Just realized that this is redundant with mesoscale_connectivity.ipynb. I'll edit that file to include this code and then delete this notebook.

[Figures](figures/) - holds all figure files created by figure analysis files.

Previous Files:

hub_spoke_sandbox.ipynb - produces one of the primacy plots (fig. 3A) but that code is buried in the second section. This notebook has a lot of extra junk that needs to get cleared out and Rhessa's code to create figure 3B needs to be incorporated. File should be renamed when that happens.
