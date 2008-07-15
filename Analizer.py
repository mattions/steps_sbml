import sys
import cPickle
import io
import numpy
import os


print sys.argv
def usage():
    print "Provide me the path to the file to analyze"
    print "Analyzer.py Sims/Sim_# with # Number of the simulation"
    print "Analyzer.py Sims/Sim_# True will run in batch mode"

dir = ''
batch = False
if (len(sys.argv) == 2):
    dir = sys.argv[1]

elif(len(sys.argv) == 3):
    dir = sys.argv[1]
    batch = sys.argv[2]
    
else:
    usage()
    exit() ## It will die if run on ipython
    sys.exit(1) 
    
## Setting the backend
import matplotlib
if batch:
    matplotlib.use('Cairo')
    print "Switching backend to Cairo. Batch execution"
from pylab import *

import visual

storage = io.loader.loadStorage(dir)

#Unpacking the storage
it = storage.getIterations() 
results = io.loader.loadRes(dir, it)
tpnt = storage.getTpnt()
legendDict = storage.getLegendDict()
species = storage.getSpecies()
vol = storage.getVol()

speciesWithInitialConc = [] # Only the specs with init conc != 0

for specie in species:
    if (species[specie] != 0):
        speciesWithInitialConc.append(specie) 
#print speciesWithInitialConc

resList = []

for k in results:
    resList.append(results[k])
    


#create figs

p = visual.Plotter(legendDict, tpnt, vol, dir)

resMean = p.calcMean(resList)

p.plotMols(['Ca'],  resMean)
p.plotMolIt('D', resList)

#p.plotMols(['D','D34','D75','D137','Ca', 'cAMP', 'PKA'], resMean)
p.plotMolsTogether(['cAMP', 'Ca', 'PKA','D'], resMean, species)
if not batch:
    show()
    
#D75list = p.createListD('75', species)
#resSum = p.calcDsumArray(D75list, resMean)
#saveFig('Calcium.png', dir)

#for specie in legendDict:
#    p.plotMol(res,tpnt, specie, legendDict)