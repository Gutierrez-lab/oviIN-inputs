import pandas as pd
from neuprint import Client
from dotenv import load_dotenv
import os
import sys

sys.path.append('../')
from get_connectome import get_connectome, connectome_to_undirected

"""
Generate Edgelist for OviInr Connectome

This script retrieves the connections for traced uncropped inputs for the OviInr
from the NeuPrint database and outputs them as an undirected edgelist.

Output Specifications:
- File: 'oviInr_traced_uncropped_inputs.txt'
- Format: Two-column edgelist (source, target), no headers.
- Excludes main neurons.

The authorization token for the NeuPrint API is loaded from a '.env' file. 
Set the NEUPRINT_AUTH_TOKEN variable in your .env before running the script.

"""

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve authorization token from the .env file
    neuprint_token = os.getenv("NEUPRINT_AUTH_TOKEN")


    # Body ID and Client initialization
    oviINr_bodyID = 423101189
    c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token=neuprint_token)

    # Get the connectome data
    connectome = get_connectome(oviINr_bodyID, exclude_main_neurons=True,
                                connectome_scope='input',
                                only_traced=True,
                                only_noncropped=True)

    # Convert to undirected graph and save to a file
    undirected_graph = connectome_to_undirected(connectome)
    undirected_graph.to_csv('oviInr_traced_uncropped_inputs.txt', index=False, header=False)
