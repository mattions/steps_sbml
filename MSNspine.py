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


######
# Wrapping the sim object in the number of iteration

iterations = 2

# Directory where to store the simulation
currentDir = io.loader.createDir()
interval = 50 #(Time of updating)
simMan = c.SimulationManager(nSec, dt_exp, species, iterations, currentDir, interval)

inputCa = []
secOfInput = 150
#duration = 2
for i in xrange(10):    

    delay = 4
#    for j in xrange(duration):
    inputTime = secOfInput * simMan.timePointIncrement
    input = c.Input(inputTime, 'Ca', 2300)
    #print "Input in at sec %f with dt time point %f" %(secOfInput, simMan.dt)
    inputCa.append(input)
#    secOfInput += duration + delay
    secOfInput += delay


input6 = c.Input(100 * simMan.timePointIncrement , 'cAMP', 3975)

#inputs = [] # Steady State
#inputs = [input1, input2, input3, input4, input5]
#inputs = [input1, input2, input3, input4, input5, input6]
inputs = [input6]
inputs.extend(inputCa)
#inputs = [] #Decomment for base line

myThreads = []
# We need to create a sim object for each iteration



stochastic = True
integrationDT = 1.0e-4

if stochastic :
    # Normal STEPS engine. Stochastic
    import steps.wmdirect as swmEngine
    
else:
    # Deterministic
    import steps.wmrk4 as swEngine
    iterations = 1 # Only one iteration.
    
for it in xrange (iterations):
    sim = swmEngine.Solver(mdl, mesh, r)
    if not stochastic :
        sim.setDT(integrationDT) # Setting the dt
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

fInfo = open(currentDir + "/info.txt", 'w')
type = ""

fInfo.write('Simulation:\n\ Sec: %d\
    \n resolution dt: %f\
    \n iterations: %d\n'  %(nSec, simMan.dt, iterations))

if stochastic:
    fInfo.write('type = stochastic\n')
else:
    fInfo.write('type = deterministic \n\
    integration dt: %f\n' %integrationDT)
   
for inp in inputs:
    inputInfo = "time: %d\tmol: %s\tquantity:%d\n" % (inp.getInputTimePoint() 
                                                      / simMan.timePointIncrement, 
                                                      inp.getMol(),
                                                      inp.getQuantity())
    fInfo.write(inputInfo)
fInfo.close()

print "Simulation Ended. Path to Simulation Files %s" %simMan.currentDir
print "Cookies ready."
