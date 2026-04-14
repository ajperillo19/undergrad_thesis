import pythia8
import fastjet
import numpy as np
import awkward as ak
import vector
import matplotlib.pyplot as plt
import random
import pickle
import gzip
from typing import List, Tuple, Dict, Union, Sequence, Any  

def fastjet_antikt_clustering(in_filename:str, out_filename:str):

    def _open_pickle(path: str):
        with open(path, "rb") as f:
            return pickle.load(f)       
        
    particle_list = _open_pickle(in_filename)
    jetdef = fastjet.JetDefinition(fastjet.antikt_algorithm, .4) # Anti-kT Clustering with R = .4
    vector.register_awkward()
    jpt=[];jpx=[];jpy=[];jpz=[];jE=[];jeta=[];jphi=[];cpt=[];ceta=[];cphi=[];cpx=[];cpy=[];cpz=[];cmass=[];ccharge=[];cmother=[]
    # delr=[];
    pdg=[]; Event_counter = []
    num_events = len(particle_list)
    batches = ak.Array([i for i in range(num_events) if i%1000==0])
    batches = ak.concatenate([batches,num_events])
    for i in range(len(batches)):
        if i+1 < len(batches):
            partial_list=ak.Array(particle_list[batches[i]:batches[i+1]],with_name="Momentum4D")
            partial_cluster=fastjet.ClusterSequence(partial_list, jetdef)
            jpt_cut=10
            jet_output=partial_cluster.inclusive_jets(min_pt=jpt_cut)
            jpx.append(ak.Array(jet_output,with_name="Momentum4D").px)
            jpy.append(ak.Array(jet_output,with_name="Momentum4D").py)
            jpz.append(ak.Array(jet_output,with_name="Momentum4D").pz)
            jE.append(ak.Array(jet_output,with_name="Momentum4D").E)
            jpt.append(ak.Array(jet_output,with_name="Momentum4D").pt)
            jeta.append(ak.Array(jet_output,with_name="Momentum4D").eta) #PSEUDORAPIDITY
            jphi.append(ak.Array(jet_output,with_name="Momentum4D").phi)
            
            constituent_output=partial_cluster.constituents(min_pt=jpt_cut)
            cpt_cut=0.2 ##

            cpt.append(([constituent_output[i]["pt"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))]))
            ceta.append([constituent_output[i]["eta"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))])
            cphi.append([constituent_output[i]["phi"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))])
            ccharge.append([constituent_output[i]["charge"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))])
            cmother.append([constituent_output[i]["mp"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))])
            # Event_counter.append([constituent_output[i]["Event_Count"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))])
            pdg.append([constituent_output[i]["pdg"][constituent_output[i]["pt"]>cpt_cut] for i in range(len(constituent_output))])

            FinalStateCluster = ak.concatenate(jpt),ak.concatenate(jeta),ak.concatenate(jphi),ak.concatenate(cpt),ak.concatenate(ceta),ak.concatenate(cphi),ak.concatenate(ccharge),ak.concatenate(cmother),ak.concatenate(pdg)

    with open(out_filename, "wb") as f:
        pickle.dump(FinalStateCluster, f)
        print(f"[cluster] saved {out_filename}")

    return ak.concatenate(jpt),ak.concatenate(jeta),ak.concatenate(jphi),ak.concatenate(cpt),ak.concatenate(ceta),ak.concatenate(cphi),ak.concatenate(ccharge),ak.concatenate(cmother),ak.concatenate(pdg)


# run in the same directory where batch_00.pkl.gz ... batch_39.pkl.gz live
if __name__ == '__main__':
    for i in range(40):
        in_file  = f"batch_{i:02d}.pkl.gz"
        out_file = f"clustered_{i:02d}.pkl"
        try:
            fastjet_antikt_clustering(in_file, out_file)
        except Exception as e:
            print(f"Error clustering {in_file}: {e}")
