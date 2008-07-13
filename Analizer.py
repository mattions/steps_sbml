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
    print "Analyzer.py Sims/Sim_# True will run in batch mode"

dir = ''
savePlot = False
if (len(sys.argv) == 2):
    dir = sys.argv[1]

elif(len(sys.argv) == 3):
    dir = sys.argv[1]
    savePlot = sys.argv[2]
    
else:
    usage()
    exit() ## It will die if run on ipython
    sys.exit(1) 
    


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

def saveFig(fig, dir):
    # Directory to save the plots
    plotDir = "%s/plots" %dir

    if (not os.path.exists(plotDir)):
        os.mkdir(plotDir)
        
    pathFig = "%s/%s" %(plotDir, fig)
    if (not os.path.exists(pathFig)):
        savefig(pathFig)
        print "Figure saved in %s" %(pathFig)


#p.create_graph(speciesWithInitialConc, resMean, savePlot)
p.plotMols(['D','D34','D75','D137','Ca', 'cAMP', 'PKA'], resMean, savePlot)
p.plotMols(['Ca', 'PP2B', 'PP2Binactive', 'PP2BinactiveCa2'], resMean, savePlot)
p.plotMols(['Ca'],  resMean, savePlot)
p.plotMolIt('D', resList, savePlot)
#saveFig('Calcium.png', dir)

#for specie in legendDict:
#    p.plotMol(res,tpnt, specie, legendDict)