# :one: Welcome!
---

**`undergrad_thesis'** is a collection of python modules that I used during the making of my undergraduate thesis. For my thesis, I worked under Sevil Salur simulating
ep collisions with initial kinematics that are representative of proposed beam energy settings for the future Electron-Ion Collider (EIC). The main focus of
my thesis was investigating the jets created in these events, specifically how one can use generalized angularity functions (GAFs) to distinguish between quark-
and gluon-initiated jets.

# :two: Workflow
---

The workflow for this thesis can be decomposed into three primary objectives:
1. Generating events in Pythia8
2. Applying the anti-kt jet clustering algorithm provided by FastJet
3. Analyzing pure event and jet information

Therefore, in this repository you will find **pythia_gen.py** which generates 1M events in batches of 25k, thus producing 40 pickle files. This is done for memory management as
I found that trying to generate 1M events continuously would crash my kernel. Moreover, **clust_gen.py** applies the anti-kt clustering algorithm to these pickle files. 
**analysis.py** then performs a physics analysis on these files.
