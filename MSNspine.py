from libsbml import *
import cPickle
import sys
import io
import control as c
import sbmlImporter
import steps.model as smodel
import steps.geom.wm as swm

#####
# Usage script to run one simulation
def usage():
    print "Give me three args: the number of sec to simulate and the dt" 


#####
# Grabbing the argument

if (len(sys.argv) != 3): # Two arguments + the name of the script
    print usage()
    exit() # For ipython
    sys.exit()

nSec = int(sys.argv[1]) #sec
dt_exp = int(sys.argv[2]) 

#############
# STEP Setup
############

# Setting the kinetic simulation

mdl = smodel.Model()

############ 
#### STEPS geometry


# setting the geometry

mesh = swm.Geom()
comp = swm.Comp('comp', mesh)
comp.addVolsys('vsys')
# Setting the Volume
volsys = smodel.Volsys('vsys', mdl)


#Importing things from the SBML
#
sbmlFile = "BIOMD0000000152.xml"
iSbml = sbmlImporter.Interface(sbmlFile)

volComp = iSbml.getVolume()

# Convert the volume to METER (Native unit of STEPS
# 1 l = 10^-3 m
volComp = volComp * pow(10,-3)
comp.vol = volComp

# Getting the variuos species
species = iSbml.getSpecies() #Dict specie --> concentration

mols = iSbml.setMols(smodel, mdl, species) # Name Specie --> Mols in STEPS

reactions = iSbml.getReactions(mols)

print "reactions : %d " %len(reactions)
for r in reactions:
    
    # Adding the reactions
    kreac = smodel.Reac(r.getName(), volsys, lhs = r.getLhs(), rhs = r.getRhs())
    
    # Setting the value for The Calcium
    # This is a bloody hack untill everything is ok
    if ( len (r.getReacts()) == 0 and
    len(r.getProds()) == 1 and 
    'Ca' in r.getProds() ):
        r.setKValue(15)
        print "Reaction %s reacts: %s prods %s k Name: %s \
        k Value: %e" % (r.getName(), r.getReacts(), 
                                                         r.getProds(), r.getKName(),
                                                         r.getKValue()) 
    kreac.kcst = r.getKValue()
    print r.getName(), r.getReacts(), r.getProds(), r.getKName(), r.getKValue()
# Destroy the reactions to free memory
del(reactions)

import steps.rng as srng
r = srng.create('mt19937', 512)
r.initialize(23412)

import steps.wmdirect as swmdirect



######
# Wrapping the sim object in the number of iteration


iterations = 1


input1 = c.Input(490001, 'Ca', 2300)
input2 = c.Input(480001, 'Ca', 2300)
input3 = c.Input(470001, 'Ca', 2300)
input4 = c.Input(460001, 'Ca', 2300)
input5 = c.Input(450001, 'Ca', 2300)

inputCa = []
startTime = 450001
for i in xrange(10):    
    if i == 0:
        input = c.Input(startTime, 'Ca', 2300)
    else:
        startTime += 2000
        input = c.Input(startTime, 'Ca', 2300)
        
    inputCa.append(input)

input6 = c.Input(400001, 'cAMP', 4000)

#inputs = [] # Steady State
#inputs = [input1, input2, input3, input4, input5]
#inputs = [input1, input2, input3, input4, input5, input6]
inputs = [input6]
inputs.extend(inputCa)

# Directory where to store the simulation
currentDir = io.loader.createDir()

simMan = c.SimulationManager(nSec, dt_exp, species, iterations, currentDir)

myThreads = []
# We need to create a sim object for each iteration
for it in xrange (iterations):
    
    sim = swmdirect.Solver(mdl, mesh, r)
    iter = simMan.inputsIn(sim, inputs, it)
    myThreads.append(iter)
    iter.start()
    
for t in myThreads:
    t.join()
    
    
io.loader.saveCommon(currentDir, simMan.tpnt, simMan.legendDict, species, iterations)
### Write some interesting value for the simulation

fInfo = open(currentDir + "/info.txt", 'w')
fInfo.write('Simulation:\n nSec: %d\n iterations: %d\n'  %(nSec, iterations))
for inp in inputs:
    inputInfo = "time: %d\tmol: %s\tquantity:%d\n" % (inp.getInputTimePoint(), 
                                                      inp.getMol(),
                                                      inp.getQuantity())
    fInfo.write(inputInfo)
fInfo.close()

print "Simulation Ended. Path to Simulation Files %s" %simMan.currentDir
print "Cookies ready."