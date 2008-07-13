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


import libsbml
import sys
import os
from Reaction import *


class Interface(object):
    
    def __init__(self, filename):
        self.__reader = libsbml.SBMLReader()
        self.__document = self.__reader.readSBML(filename)
        self.__model = self.__document.getModel()
        if self.__document.getNumErrors() > 0 :
            pm = self.__document.getError(0)
            if pm.getErrorId() == libsbml.XMLFileUnreadable:
                print "Sbml File %s not found or unreadable in dir %s" %(filename, 
                                                                         os.getcwd()) 
                sys.exit(1)
        self.__globalParameters = self.parseGlobalParameters()
            
    
    def getVolume(self):
        """
            Return the volume of the compartment
        """
        ListOfComp = self.__model.getListOfCompartments()
        
        # getting the volume of the compartment
        volComp = 0
        if len (ListOfComp) == 1:
            volComp = ListOfComp[0].getVolume()
        else:
            print "ERROR: It's supported only one compartment.  \
            Compartments in this model: %d" %len(ListOfComp)
            sys.exit(1)
        self.__volComp = volComp
        return volComp
    
    def getSpecies(self):
        """
            Return the dictionary with the species and their own concentration
        """
        #getting the variuos species
        ListOfSpecies = self.__model.getListOfSpecies()
        species = {}
        for specie in ListOfSpecies:
            species[specie.getId()] = specie.getInitialConcentration()
        return species
    
    def setMols(self, smodel, mdl, species):
        """
        Return the mols dictionary that map the name of molecule and the 
        STEP mol object
            
        :Parameters:
            smodel
                The STEP container for all the model info
            mdl
                The model itself in STEP
            species
                The Species to add to the model
        """
        mols = {}
        for specie in species:
            mol = smodel.Spec(specie, mdl)
            mols[specie] = mol 
        return mols
            
            
    def getReactions(self, mols):   
        listOfReactions = self.__model.getListOfReactions()
        reactions = []
        for i in xrange(len(listOfReactions)):
            r = Reaction()
            r.setName("React_" + str(i))
            
            # Reactants
            reacts = []
            lhsList = [] # Left side STEPS
            reactants = listOfReactions[i].getListOfReactants()
        
            for reactant in reactants:
                sto = reactant.getStoichiometry()
                for j in xrange(int(sto)):
                    if(reactant.getSpecies() != "Empty"):
                        reacts.append(reactant.getSpecies())
                        # Adding the mol Obj from STEPS
                        lhsList.append(mols[reactant.getSpecies()])  
            r.setReacts(reacts)
            r.setLhs(lhsList)
        
            # Products 
            prods = []
            rhsList = [] # Right side STEPS
            products = listOfReactions[i].getListOfProducts()
            
            for product in products:
                
                sto = product.getStoichiometry()
                for j in xrange(int(sto)):
                    if(product.getSpecies() != "Empty"):
                        prods.append(product.getSpecies())
                        rhsList.append(mols[product.getSpecies()])
                    
            r.setProds(prods)
            r.setRhs(rhsList)
            
            # Kinetik constants
            params = {}
            kLaw = listOfReactions[i].getKineticLaw()
            
            ## Getting the math
#            math = kLaw.getMath()
#            numc = math.getNumChildren()
#            print numc
#            if (numc > 1):
#                child = math.getLeftChild()
#                print child.getName()
#                i = 1
#                for i in xrange(numc -1):
#                    print math.getChild(i).getName()
            
            parameters = kLaw.getListOfParameters()
            for p in parameters:
                r.setKName(p.getId())
                
                if p.getId() in self.__globalParameters: # Overwrite the local 
                                                         # with the global
                    params[p.getId()] = self.__globalParameters[p.getId()]
                    r.setKValue(self.__globalParameters[p.getId()])
                else:
                    params[p.getId()] = p.getValue()
                    r.setKValue(p.getValue())
            reactions.append(r)
        return reactions
    
    def parseGlobalParameters(self):
        listOfParameters = self.__model.getListOfParameters()
        globPar = {}
        for par in listOfParameters:
            globPar[par.getId()] = par.getValue()
            print par.getId(), par.getValue()
        return globPar
    
