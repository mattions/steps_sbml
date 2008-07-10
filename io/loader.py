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
stoName = '/storage'

# dir
today = datetime.date.today()
dir_date = "Sims/%s" %today

def saveStorage(dir, storage):
    """
    Save the storage object in the directory provided
    
    :Params:
        dir 
            Directory where to save the object
        storage
            The object to save
    """
    FILE = open(dir + "/" + stoName, 'w')
    cPickle.dump(storage, FILE, 1)
    FILE.close()
    
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
        try:
            FILE_RES = open(dir + "/" + resName, 'r')
            res = cPickle.load(FILE_RES)
            FILE_RES.close()
            results[i] = res
            print "loaded file %s/%s" %(dir, resName)
        except:
            print "Impossible to load file %s/%s\t Skipped." %(dir, resName)
    return results


def loadStorage(dir):

    FILE = open(dir + stoName, 'r')
    storage = cPickle.load(FILE)
    FILE.close()
    print "loaded file %s%s" %(dir, stoName)
    return storage