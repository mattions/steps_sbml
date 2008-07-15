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

from pylab import *
import numpy
import os
import re


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

    def createListD(self, molName, species):
        list = []

        p = re.compile('\w*' + molName + '\w*')
        for specie in species:
            m = p.match(specie)
            if m:
                list.append(m.group())
        return list
    
    def calcSumArray(self, arraylist, res):

       
        resSum = numpy.zeros(self.__tpnt.shape)
        for item in arraylist:
            molIndex = self.__legendDict[item]
            resSum += res[:,molIndex]
        return resSum
        
        
    def plotMols(self, mols, res, conc = False):
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
        
    def createSimilarDict(self, species):
        
        dict = {}
        molTogroup = ['34','75','137']
        for mol in molTogroup:
            p = re.compile('\w*' + mol + '\w*')
            list = []
            for specie in species:
                m = p.match(specie)
                if m:
                    list.append(m.group())
            dict[mol] =list
        return dict

    def plotMolsTogether(self, mols, res, species, conc = False):
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
        
        molToGroup = self.createSimilarDict(species)
        for mol in mols:
              self.plotRoutine(res[:,self.__legendDict[mol]], conc)
              
        resMol = self.calcSumArray(molToGroup['34'], res)
        self.plotRoutine(resMol, conc)

        resMol = self.calcSumArray(molToGroup['75'], res)
        self.plotRoutine(resMol, conc)

        resMol = self.calcSumArray(molToGroup['137'], res)
        self.plotRoutine(resMol, conc)
        
        mols.append('D34')
        mols.append('D75')
        mols.append('D137')  
        
        legend(mols)
        xlabel('Time (sec)')
        title(mols)
        self.saveFig(str(mols) + ".png")

    def plotRoutine(self, res, conc):
       if conc is True:
           plot(self.__tpnt, self.calcConc(res))
           ylabel('#concentrations')
       else:
           plot(self.__tpnt, res)
           ylabel('#molecules')
        
    def plotMolIt(self, mol, resList, conc = False):
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
            savefig(pathFig, dpi='300')
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