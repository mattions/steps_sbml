# loader.py
"""
 * Copyright (C) 2008 Jun - Michele Mattioni:
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

"""
Used to define all the function to store and load the python serialezed objects
"""

import cPickle
import os
import datetime

# Variable for the name
tName = '/timepoints'
lName = '/legendDict'
sName = '/spec_conc'
itName = '/iterations'

# dir
today = datetime.date.today()
dir_date = "Sims/%s" %today


def saveCommon(dir, tpnt, legendDict, species, iterations):
    """
        Save all the res array, the timepoints, the legendDict and the spec_con
        :param:
            dir
                The directory where to nest the Simulation directory.
            timepoints
                The timepoints
            legendDict
                The legend to map the number of the row of the result with the 
                name of the Mol
            species 
                The species that has started the simulation mapped to their 
                initial concentration
    """
    
    FILE_TPOINTS = open(dir + tName, 'w')
    FILE_LEGEND = open(dir + lName,'w')
    FILE_SPEC_CONC = open(dir + sName, 'w')
    FILE_IT = open(dir + itName, 'w')

    cPickle.dump(tpnt, FILE_TPOINTS, 1)
    cPickle.dump(legendDict, FILE_LEGEND, 1)
    cPickle.dump(species, FILE_SPEC_CONC, 1)
    cPickle.dump(iterations, FILE_IT, 1)
    
    FILE_TPOINTS.close()
    FILE_LEGEND.close()
    FILE_SPEC_CONC.close()
    FILE_IT.close()

def saveRes(dir, res, resName):
    print "Saving result for %s" %resName
    
    FILE_RES = open(dir + "/" + resName, 'w')
    cPickle.dump(res, FILE_RES, 1)
    FILE_RES.close()
    
    
def createDir():
    """
        Create the directory where to put the simulation
    """
    free = False
    index = 0
    dir = "%s/Sim_%d" %(dir_date, index)
    while not free :
        if os.path.exists(dir):
            index = index + 1
            dir = "%s/Sim_%d" %(dir_date, index)
        else:
            free = True
            os.makedirs(dir)
    return dir
    
def loadRes(dir, iterations):
    """
        Load the result array
        :param:
            dir 
                The directory of the simulation
            iterations
                The iterations performed        
    """
    results = {}
    for i in xrange(iterations):
        resName = "res_" + str(i)
        FILE_RES = open(dir + "/" + resName, 'r')
        res = cPickle.load(FILE_RES)
        FILE_RES.close()
        results[i] = res
        print "loaded file %s/%s" %(dir, resName)
    return results



def loadTimePoints(dir):
    """
        Load the timepoints array
        :param:
            dir The directory of the simulation
    """
    FILE_TPOINTS = open(dir + tName, 'r')
    tpnt = cPickle.load(FILE_TPOINTS)
    FILE_TPOINTS.close()
    print "loaded file %s%s" %(dir, tName)
    return tpnt

def loadLegendDict(dir):
    """
        Load the legend Dictionary 
        :param:
            dir The directory of the simulation
    """
    FILE_LEGEND = open(dir + lName,'r')
    legendDict = cPickle.load(FILE_LEGEND)
    FILE_LEGEND.close()
    print "loaded file %s%s" %(dir, lName)
    return legendDict
    
def loadSpecConc(dir):
    """
        Load the Spec conc Dictionary
        :param:
            dir The directory of the simulation
    """
    FILE_SPEC_CONC = open(dir + sName, 'r')
    species = cPickle.load(FILE_SPEC_CONC)
    FILE_SPEC_CONC.close()
    print "loaded file %s%s" %(dir, sName)
    return species

def loadIterations(dir):
    """
        Load the iterations
        :param:
            dir The directory of the simulation
    """
    FILE_IT = open(dir + itName, 'r')
    iterations = cPickle.load(FILE_IT)
    FILE_IT.close()
    print "loaded file %s%s" %(dir, itName)
    return iterations
    