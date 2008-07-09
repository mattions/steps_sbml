from pylab import *
import numpy


class Plotter(object):
    """
        Provide a set of ready to use plotting facility
    """
    def __init__(self, legendDict, tpnt, vol):
        self.speciesFromUser = ['D','D34','D75','D137','Ca', 'cAMP', 'PKA']
        self.__legendDict = legendDict
        self.__tpnt = tpnt
        self.specInt = ['D','D34','D75', 'D137','Ca','cAMP', 
                                    'PKA','PP2Binactive', 'PP2B', 'D34_75', 
                                    'D34_137', 'CDK5', 'PP2A', 'PP2C']
        self.__vol = vol

    
    def create_graph(self, speciesWithInitialConc, res):
        """
            Create a graph with all the Species
        """
        figure()
        speciesToPlot = list(self.speciesFromUser)
        speciesToPlot += speciesWithInitialConc
        ## Delete duplicates
        speciesToPlot = set(speciesToPlot)
        for specie in self.__legendDict:
            if (speciesToPlot.__contains__(specie) ):
               plot(self.__tpnt, res[:,self.__legendDict[specie]])
    
        #legend(speciesToPlot)
        xlabel('Time (sec)')
        ylabel('#molecules')
        title (speciesWithInitialConc)
        show()
        
    def plotMols(self, mols, res, conc = False):
        figure()
        for mol in mols:
            if conc is True:
                plot(self.__tpnt, self.calcConc(res[:,self.__legendDict[mol]]))
                ylabel('#concentrations')
            else:
                plot(self.__tpnt, res[:,self.__legendDict[mol]])
                ylabel('#molecules')
        legend(mols)
        xlabel('Time (sec)')
        title(mols)
        
        
    def plotMol(self, mol, res, conc = False):
        """
            Plot only Calcium
        """
        
        figure()
        if conc is True:
            plot(self.__tpnt, self.calcConc(res[:,self.__legendDict[mol]]))
            ylabel('#concentrations')
        else:
            plot(self.__tpnt, res[:,self.__legendDict[mol]])
            ylabel('#molecules')
        legend((mol,))
        xlabel('Time (sec)')
        
        title (mol)
        show()
        
    def plotMolIt(self, mol, resList):
        """
            Plot a molecule in a set of iterations
            :parameters:
                mol
                    The molecule to plot
                resList
                    The list of the result array to plot
        """
        
        figure()
        for res in resList:
            if conc is True:
                plot(self.__tpnt, self.calcConc(res[:,self.__legendDict[mol]]))
                ylabel('#concentrations')
            else:
                plot(self.__tpnt, res[:,self.__legendDict[mol]])
                ylabel('#molecules')
        legend((mol,))
        xlabel('Time (sec)')
        title ("iteration plotted " + str(len(resList)))
        
    def calcMean(self, resList):
        """
        Return the mean of a list of array
        
        :Parameters:
            resList
                List of array of which we have to calculate the mean
                
        """
        s = resList[0].shape
        resMean = numpy.zeros(s)
        for i in xrange(len(resList)) :
            resMean += resList[i]
        resMean /= len(resList)
        return resMean
    
    def calcConc(self, numMol):
        NAv = 6.023 * pow(10,23)
        conc = numMol / (self.__vol * NAv)
        return conc