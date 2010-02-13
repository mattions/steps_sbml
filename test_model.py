# Author Michele Mattioni
# date Sat Feb 13 11:21:00 GMT 2010

NITER = 2
ENDTIME = 200
DT = 0.001
POINTS = int(ENDTIME/DT)


import steps.model as smodel
import steps.geom as swm
import steps.rng as srng
import steps.solver as ssolver
import sbmlImporter
import numpy as np

# Setting the kinetic simulation

mdl = smodel.Model()

mesh = swm.Geom()
comp = swm.Comp('comp', mesh)
comp.addVolsys('vsys')
# Setting the Volume
volsys = smodel.Volsys('vsys', mdl)

sbmlFile = "BIOMD0000000005.xml"
iSbml = sbmlImporter.Interface(sbmlFile)

volComp = iSbml.getVolume()
# Convert the volume to METER (Native unit of STEPS
# 1 l = 10^-3 m
volComp = volComp * pow(10,-3)
comp.vol = volComp

species = iSbml.getSpecies() #Dict specie --> concentration


molecules = iSbml.setMols(smodel, mdl, species) # Name Specie --> Mols in STEPS

reactions = iSbml.getReactions(molecules)

iSbml.instantiate_reaction(smodel, volsys, reactions)


############ 

r = srng.create('mt19937', 256)
r.initialize(7233)

tpnt = np.arange(0.0, ENDTIME, DT)
res_m = np.zeros([NITER, POINTS, len(species)])
legendDict = {}

print "Setting up the model"
sim = ssolver.Wmdirect(mdl, mesh, r)


print "before simulation"
for it in range (0, NITER):
    sim.reset()
    iSbml.set_initial_conditions(sim, species)                       
    for t in xrange(0,POINTS):
        sim.run(tpnt[t])
        i = 0
        for specie in species:
                res_m[it, t, i] = sim.getCompCount('comp', specie)
                legendDict[specie] = i
                i = i + 1

mean_res = np.mean(res_m, 0)
