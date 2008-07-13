
class Storage(object):
    
    def __init__(self, currentDir, tpnt, legendDict, species, iterations, vol):
        self.__currentDir = currentDir
        self.__tpnt = tpnt
        self.__legendDict = legendDict
        self.__species = species
        self.__iterations = iterations
        self.__vol = vol

    def getCurrentDir(self):
        return self.__currentDir


    def getTpnt(self):
        return self.__tpnt


    def getLegendDict(self):
        return self.__legendDict


    def getSpecies(self):
        return self.__species


    def getIterations(self):
        return self.__iterations
    
    def getVol(self):
        return self.__vol
    
    currentDir = property(getCurrentDir, None, None, "Directory where the Sims are seved")

    tpnt = property(getTpnt, None, None, "Timepoints")

    legendDict = property(getLegendDict, None, None, "The map with the number of \
    the specie and the mol object in STEPS")

    species = property(getSpecies, None, None, "The map of name ID and the number of species")

    iterations = property(getIterations, None, None, "Number of iterations")
    
    vol = property(getVol, None, None, "Volume of the simulation")

 

        
