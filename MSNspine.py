
# -*- coding: utf-8 -*-

"""
 * Copyright (C) 2008 Jul - Michele Mattioni:
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, 
 * Boston, MA  02110-1301  USA
"""

from libsbml import *
import sys
import os
import io
import control as c
import sbmlImporter
import steps.model as smodel
import steps.geom as swm

#####
# Usage script to run one simulation
def usage():
 
    print "\npython MSNspine.py 800 -3 sto"
    print "python MSNspine.py 800 -3 det 1e-4"
    print "Two possible simulation are available: deterministic or stochastic.\
    \n- First argument is the number of the seconds you want to simulate\
    \n- Second argument is the resolution of the the points.\
    \n- Third argument is the type of simulation. det for deterministic, sto for stochastic.\
    \n- Fourth argument is the integration dt for the deterministic simulation.\
    Is not needed in the case of stochastic one." 


#####
# Grabbing the argument

if len(sys.argv) == 5: # Only if deterministic
    deterministicIntegrationDT = float(sys.argv[4])
    
elif len(sys.argv) != 4: # If it's not 4 it's WRONG so we exit
    print usage()
    exit() # For ipython
    sys.exit()

nSec = int(sys.argv[1]) #sec
dt_exp = int(sys.argv[2]) # Resolution point
typeOfSimulation = sys.argv[3] #type

#===========
# Log and error Setting the log and the error file 
# Directory where to store the simulation
#============
currentDir = io.loader.createDir()
print "Simulation results will be stored in : %s" %currentDir

saveOut = sys.stdout
saveErr = sys.stderr

logFile = open(os.path.join(currentDir,'log.txt'), 'w')
errorFile = open(os.path.join(currentDir,'error.txt'), 'w')
sys.stdout = logFile
sys.stderr = errorFile


print "Simulation started with the following aguments:"
print sys.argv

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
    

    # Hack for the k to get the Volume right
    # EXPERIMENTAL -- HAS TO BE DONE WITH THE MATH
    
    if (len(r.getReacts()) < 1) :
        oldK =  r.getKValue()
        newK = r.getKValue() * volComp
        r.setKValue(newK)
        print "Reaction %s reacts: %s prods %s k Name: %s \
        k NEW Value: %e k OLD Value: %e" % (r.getName(), r.getReacts(), 
                                                         r.getProds(), r.getName(), newK,
                                                         oldK)
        
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

iterations = 4
simMan = c.SimulationManager(nSec, dt_exp, species, iterations, currentDir, interval = 50)

#==============================
# We need to create a sim object for each iteration
# So we import the eingine with the same name and we create an
# instance each iteration

import steps.solver as ssolver

# Creating the threads        
myThreads = []
## Experiments
experiment = c.Experiment(simMan) # General controller for the experiment
inputs = [] #Inputs. Var used for printing the inputs
if typeOfSimulation == 'det' :
    iterations = 1 # Only one iteration.

for it in xrange (iterations):
    if typeOfSimulation == 'sto' :
        # Normal STEPS 
        sim = ssolver.Wmdirect(mdl, mesh, r) #Create the sim
    elif typeOfSimulation == 'det' :
        # Deterministic
        sim = ssolver.Wmrk4(mdl, mesh, r) #Create the sim
        sim.setDT(deterministicIntegrationDT) # Setting the dt
    else:
        print "\nError - Type of simulation not Understood. Exit.\n"
        usage()
        exit() # For ipython
        sys.exit()
        
    #==========
    # We must create a list of inputs for each simulation.
        
    #inputs = experiment.baseline() #Decomment for base line
    #inputs = experiment.rig1() # Fenandez Simulation
    inputs = experiment.rig2() # DA increasing the effect of the Glu Schultz
    #inputs = experiment.rig3() # DA increasing the effect of the Glu Fast train of Glu
    #inputs = experiment.rig4() # Simulate the release of cAMP only
    #inputs = experiment.rig5() # Release of a fast train of Calcium only.
    
    iter = simMan.inputsIn(sim, inputs, it)
    myThreads.append(iter)
    iter.start()
    
for t in myThreads:
    t.join()
    
storage = io.Storage(currentDir, simMan.tpnt, simMan.legendDict, species, 
                     iterations, volComp)
io.loader.saveStorage(currentDir, storage)    
#io.loader.saveCommon(currentDir, simMan.tpnt, simMan.legendDict, species, iterations)
### Write some interesting value for the simulation

fInfo = open(os.path.join(currentDir, "info.txt"), 'w')
type = ""

fInfo.write('Simulation:\nSec: %d\
    \nresolution dt: %f\
    \niterations: %d\n'  %(nSec, simMan.dt, iterations))

if typeOfSimulation == 'sto':
    fInfo.write('type = stochastic\n')
elif typeOfSimulation == 'det':
    fInfo.write('type = deterministic\n\
    integration dt: %f\n' %deterministicIntegrationDT)
   
# Sort the time.
tInputs = inputs.keys()
tInputs.sort()   

for t in tInputs:
    for inp in inputs[t]:
        inputInfo = "time: %d\tmol: %s\tquantity:%d\n" % (inp.getInputTimePoint() 
                                                          / simMan.timePointIncrement, 
                                                          inp.getMol(),
                                                          inp.getQuantity())
    fInfo.write(inputInfo)
fInfo.close()

# Close the files
logFile.close()
errorFile.close()

sys.stdout = saveOut # Restoring the printing on the console
sys.stderr = saveErr # Restoring the error on the console

# Deleting the error file if no error present
if os.path.getsize(errorFile.name) == 0:
    os.remove(errorFile.name)
    print "Simulation Ended. Path to Simulation Files %s" %simMan.currentDir
    print "Cookies ready." 
else:
    print "Error Happened! - check the error File: %s" %errorFile.name
