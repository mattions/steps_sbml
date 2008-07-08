import sys
import cPickle
from pylab import *
import visual
import io
import numpy
import os

print sys.argv
def usage():
    print "Provide me the path to the file to analyze"
    print "Analyzer.py Sims/Sim_# with # Number of the simulation"

if (len(sys.argv) != 2):
    usage()
    exit() ## It will die if run on ipython
    sys.exit(1) 
    
    

dir = sys.argv[1]

it = io.loader.loadIterations(dir)
results = io.loader.loadRes(dir, it)
tpnt = io.loader.loadTimePoints(dir)
legendDict = io.loader.loadLegendDict(dir)
species = io.loader.loadSpecConc(dir)

speciesWithInitialConc = [] # Only the specs with init conc != 0

for specie in species:
    if (species[specie] != 0):
        speciesWithInitialConc.append(specie) 
#print speciesWithInitialConc

resList = []

for k in results:
    resList.append(results[k])
    


#create figs
resMean = numpy.mean(resList, 0)
p = visual.Plotter(legendDict, tpnt)

def saveFig(fig, dir):
    # Directory to save the plots
    plotDir = "%s/plots" %dir

    if (not os.path.exists(plotDir)):
        os.mkdir(plotDir)
        
    pathFig = "%s/%s" %(plotDir, fig)
    if (not os.path.exists(pathFig)):
        savefig(pathFig)
        print "Figure saved in %s" %(pathFig)
    
p.create_graph(speciesWithInitialConc, resMean)
p.plotMols(['D','D34','D75','D137','Ca', 'cAMP', 'PKA'], resMean)
p.plotMols(['Ca', 'PP2B', 'PP2Binactive', 'PP2BinactiveCa2'], resMean)
saveFig('interestingSpecies.png', dir)
p.plotMol('Ca',  resMean)
#saveFig('Calcium.png', dir)

#for specie in legendDict:
#    p.plotMol(res,tpnt, specie, legendDict)