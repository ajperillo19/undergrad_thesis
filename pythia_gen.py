import pythia8
import fastjet
import numpy as np
import awkward as ak
import vector
import matplotlib.pyplot as plt
import random
import pickle
from typing import List, Tuple, Dict, Union, Sequence, Any

def pythia_generator(num_events, out_filename:str):
    ak_particle_list=[];fsp_list=[];electro_list=[]
    seed = np.random.randint(1,10000000,dtype=int) #change made 2/10 moved under runs and increased number
    eta_cut = 7
    temp=[];tempfsp=[];tempelectro=[]
    event_list=[]

    pythia = pythia8.Pythia()
    pythia.readFile("/home/ajperillo19/anaconda3/envs/EIC_ENV/CustomEICTune.cmnd") # customize beam settings
    pythia.readString("Random:setSeed =true")
    pythia.readString("Random:Seed =" +str(seed))

    pythia.init()
    count = 0
    for runs in range(num_events):
        seed = np.random.randint(1,10000000,dtype=int) ###
        count += 1
        if len(temp)>0:
            ak_particle_list.append(temp)

        if len(tempfsp)>1 and len(tempelectro)==1:
            fsp_list.append(tempfsp);electro_list.append(tempelectro)
        temp=[];tempfsp=[];tempelectro=[]

        if not pythia.next(): continue

        for c_event in pythia.event:
            cv = c_event
            if cv.status() == -23:
                mother = cv.id()

            if c_event.isFinal() and  c_event.eta() < eta_cut and c_event.eta() > -eta_cut and c_event.phi() >= -np.pi and c_event.phi() <= np.pi:
                tempfsp.append({"pt": cv.pT(), "eta": cv.eta(), "phi": cv.phi(), "mass": cv.mCalc(), "charge" : cv.charge(),"mp":mother,"pdg":cv.id(),"px":cv.px(),"py":cv.py(),"pz":cv.pz(),"E":cv.e()})
        if len(tempfsp)>1:
            ak_particle_list.append(tempfsp)

    with open(out_filename, "wb") as f:
            pickle.dump(ak_particle_list, f)
            print(f"[pythia_generator] saved {out_filename}")

    return ak_particle_list

if __name__ == '__main__':
    for i in range (40):
        outname = f"batch_{i:02d}.pkl.gz"   # change extension to .pkl if you don't want compression
        # choose deterministic seed per batch if you want reproducibility:
        
        print("Producing", outname)
        pythia_generator(25000, out_filename=outname) # batches of 25k events -> 1M total