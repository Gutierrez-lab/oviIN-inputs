<span style="font-family:Papyrus; font-size:6em;">oviIN inputs</span>

 <span style="font-size:1.5em;">**Studying the sub-connectome induced by the inputs to oviIN. Includes scripts to process the data and produce figures.**</span>


> ## <div style="background-color:rgba(250, 230, 7, 1);"> ! Setting up the Environment 
> [environment.yaml](environment.yaml) - All packages needed to run our analyses files are included in this file. Please use conda to create this environment and please have a python version 3.11 or later.</div>

## Function Files:

[get_connectome.py](get_connectome.py) - queries the Hemibrain to obtain a sub-connectome from the inputs and/or outputs of a specified neuron or group of neurons. This function was initially written by Rhessa and modified by Gabrielle. 

[format_edgelist.py](gcm_pipeline/format_edgelist.py) - formats the sub-connectome in preparation for running modularity on it. This function was contributed by Alex. 

[modularity.py](modularity.py) - Function file for analyzing the modularity result. (**EDIT NEEDED HERE**)

[flybrain.auth.txt](flybrain.auth.txt) - File containing hemibrain key, needed for neuprint access.

[matplotlibrc](matplotlibrc) - Contains formatting choices we made for the figures. 

## Analysis Files:

[piechart.ipynb](piechart.ipynb) - produces both stacked barchart and piechart figures to analyze supercategory representation in modules. This file requires the [modularity data](modularity_runs/0.0/0-0_98765.txt) and the [supercategory](data/all_roi_df.xlsx) dataframe. 

[comparisons_to_fullHB.ipynb](comparisons_to_fullHB.ipynb) - computes both joint marginals between the whole brain data and oviIN input connectome and jaccard similarity between connectomes. Needs the input of preprocessed_nodes.csv for both oviIN connectome and whole brain connectome.

[mesoscale_connectivity.ipynb](mesoscale_connectivity.ipynb) - produces analyses about the top 33 inputs to the oviINr based on synaptic weight. Also contains code for the skeleton plots with synaptic connectivity plotted on the arbor and colored by module id that the input neuron is sorted into.

[oviposition_circuit.ipynb](oviposition_circuit.ipynb) - produces plots of synapse counts in oviposition circuit for figure 1. Needs to be cleaned up. File can be renamed after editing.

[hub_bespoke.ipynb](hub_bespoke.ipynb) - produces the primacy plots and addition statistics about the inputs of the oviIN. Both figures pull data from neuprint and the second figure requires modularity data found under .

[ovi_specs_rankings.ipynb](ovi_specs_rankings.ipynb) - produces plots of oviIN rankings within the full Hemibrain for figure 2. Figures require access to neuprint using the auth token.

[jaccard_analysis.ipynb](jaccard_analysis.ipynb) - 

[module_syn_placement.ipynb](module_syn_placement.ipynb) - 

[participation.ipynb](participation.ipynb) - 

[pooled_similarity.ipynb](pooled_similarity.ipynb) - 

## Folders: 
[figures](figures/) - holds all figure files created by analysis files and used in the manuscript.
[data](data/) - holds all data files used for analysis. 
* Dataframes in the [data/exported-traced-adjacencies](data/exported-traced-adjacencies-v1.2/) folder are pulled and saved through the Neuprint-python API. 
* Dataframes in [data/preprocessed-v1.2](data/preprocessed-v1.2/) are created from running modularity on the full hemibrain dataset and then merging on neuron data.

* [data/all_neurons_n_partners](data/all_neurons_n_partners.csv) - This file holds the information of all neurons in the hemibrain including their pre and post synaptic partners (neurons, connection weights and celltypes) with a weighted threshold at 3 connections.
* [data/all_neurons_n_partners_0weightthreshold](data/all_neurons_n_partners_0weightthreshold.csv) - This is similar but without the threshold
* [data/all_roi_df](data/all_roi_df.xlsx) - This dataframe holds supercategories of neuropils hierarchy. The primary neuropils hierarchy is pulled from the Neuprint-python API.
* [data/output_to_oviIN_primacy](data/output_to_oviIN_primacy.csv) - Contains the input weights and ranking based on the weights for every pre-synaptic cell type to the oviIN\_R
* [data/ovi_pre_syns](data/ovi_pre_syns.csv) - Contains coordinate data for all connections made onto the oviIN\_R. 
* [data/preprocessed-v1.2.zip](data/preprocessed-v1.2.zip) - Compressed version of the [preprocessed-v1.2](data/preprocessed-v1.2/) folder for easy sharing.

[gcm_pipeline](gcm_pipeline/) - hold all files and instructions needed to run the modularity analysis
* []()
* []()
* []()
* []()

[modularity_runs](modularity_runs/) - holds the results from running the gcm_pipline as well as the edgelist used for the oviINr using its input sub-connectome.
* []()