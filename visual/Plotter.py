from pylab import *


class Plotter(object):
    """
        Provide a set of ready to use plotting facility
    """
    def __init__(self, legendDict, res, resMean, tpnt):
        self.speciesFromUser = ['Ca', 'PKA', 'D34', 'D75', 'D137', 'D']
        self.__legendDict = legendDict
        self.__res = res
        self.__resMean = resMean
        self.__tpnt = tpnt
        self.specInt = ['D','D34','D75', 'D137','Ca','cAMP', 
                                    'PKA','PP2Binactive', 'PP2B', 'D34_75', 
                                    'D34_137', 'CDK5', 'PP2A', 'PP2C']

    
    def create_graph(self, speciesWithInitialConc, res):
        """
            Create a graph with all the Species
        """
        figure()
        self.speciesFromUser += speciesWithInitialConc
        ## Delete duplicates
        speciesToPlot = set(self.speciesFromUser)
        for specie in self.__legendDict:
            if (speciesToPlot.__contains__(specie) ):
               plot(self.__tpnt, res[:,self.__legendDict[specie]])
    
        #legend(speciesToPlot)
        xlabel('Time (sec)')
        ylabel('#molecules')
        title (speciesWithInitialConc)
        show()
        
    def plotMols(self, mols, res):
        figure()
        for mol in mols:
            plot(self.__tpnt, res[:,self.__legendDict[mol]])
        legend(mols)
        xlabel('Time (sec)')
        ylabel('#molecules')
        title(mols)
        
        
    def plotMol(self, mol, res):
        """
            Plot only Calcium
        """
        
        figure()
        plot(self.__tpnt, res[:,self.__legendDict[mol]])
        legend((mol,))
        xlabel('Time (sec)')
        ylabel('#molecules')
        title (mol)
        show()
        
    def plotMolIt(self, mol, it, res):
        """
            Plot only Calcium
        """
        
        figure()
        for i in xrange(len(it)):
            plot(self.__tpnt, res[i,:,self.__legendDict[mol]])
        legend((mol,))
        xlabel('Time (sec)')
        ylabel('#molecules')
        title ("iteration plotted " + str(it) )
        show()
