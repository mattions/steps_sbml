from pylab import *
import numpy
import os


class Plotter(object):
    """
        Provide a set of ready to use plotting facility
    """
    def __init__(self, legendDict, tpnt, vol, dir):
        self.speciesFromUser = ['D','D34','D75','D137','Ca', 'cAMP', 'PKA']
        self.__legendDict = legendDict
        self.__tpnt = tpnt
        self.__dir = dir
        self.specInt = ['D','D34','D75', 'D137','Ca','cAMP', 
                                    'PKA','PP2Binactive', 'PP2B', 'D34_75', 
                                    'D34_137', 'CDK5', 'PP2A', 'PP2C']
        self.__vol = vol

    
    def plotMols(self, mols, res, conc = False, batch = False):
        """
        Plot the number of all the molecules provided as list on the same graph. 
        
        :Parameters:
            mols
                The list of molecules
            res
                The array woth the concentration of each molecules
            conc
                If true the conc of the molecule will be plotted (default: False)
            batch
                It will save the graph to a directory instead of showing. (default: False)
        """
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
        self.saveFig(str(mols) + ".png")
        if batch is True:
            show(False)
        else:
            show(True)
        
    def plotMolIt(self, mol, resList, conc = False, batch = False):
        """
            Plot a molecule in a set of iterations
            :parameters:
                mol
                    The molecule to plot
                resList
                    The list of the result array to plot
                conc
                    If true the conc of the molecule will be plotted 
                    (default: False)
                batch
                    It will save the graph to a directory instead of showing. 
                    (default: False)
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
        it = len(resList)
        title ("iterations plotted: " + str(it))
        self.saveFig(str(mol) + "_it_" + str(it) + ".png")
        if batch is True:
            show(False)
        else:
            show(True)
                
    def saveFig(self, figName):
        """
        Save the figure in the Plots directory
        """
        # Directory to save the plots
        plotDir = "%s/plots" %self.__dir
    
        if (not os.path.exists(plotDir)):
            os.mkdir(plotDir)
            
        pathFig = "%s/%s" %(plotDir, figName)
        if (not os.path.exists(pathFig)):
            savefig(pathFig)
        print "Figure saved in %s" %(pathFig)
        
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