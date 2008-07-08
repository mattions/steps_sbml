from libsbml import *


class sbmlImporter(object):
    
    def __init__(self, filename):
        self.__reader = SBMLReader()
        self.__document = self.__reader.readSBML(filename)
        self.__model = self.__document.getModel()
        
    def getModel(self):
        return self.__model
        
    def getVolume(self):
        ListOfComp = self.__model.getListOfCompartments()
        #print self.__model, ListOfComp, len(ListOfComp), ListOfComp[0]
        # getting the volume of the compartment
        volComp = 0
        for com in ListOfComp:
            volComp = com.getVolume()
        
        return volComp
    #    print "VolComp %e" %volComp
    
    def getSpecies():
        #getting the variuos species
        ListOfSpecies = self.__model.getListOfSpecies()
        species = {}
        for specie in ListOfSpecies:
            species[specie.getId()] = specie.getInitialConcentration()
        return species
    
    def settingMols(self, species):
        for specie in species:
            mol = smodel.Spec(specie.getId(), mdl)
            mols[specie.getId()] = mol 
        return mols
            
            
    def getReactions(self, model):   
        
        #getting the reactions
        ListOfReactions = model.getListOfReactions()
        reac = [[], [], []]
        
        for reaction in ListOfReactions:
    		print "Reaction %d" %i
    		reacts = []
    		reactants = reaction.getListOfReactants()
    		
    		for reactant in reactants:
    			sto = reactant.getStoichiometry()
    			for i in xrange(int(sto)):
    				if(reactant.getSpecies() == "Empty"):
    					reacts.append("")
    				else:
    					reacts.append(reactant.getSpecies())
    			
    #		print reacts
    	
    		prods = []
    		products = reaction.getListOfProducts()
    		
    		for product in products:
    			
    			sto = product.getStoichiometry()
    			for i in xrange(int(sto)):
    				if(product.getSpecies() == "Empty"):
    					prods.append("")
    				else:
    					prods.append(product.getSpecies())
    				
    	#	print prods
    		
    		params = []
    		kLaw = reaction.getKineticLaw()
    		parameters = kLaw.getListOfParameters()
    		for parameter in parameters:
    			params + [parameter.getId()]
    		
    #		print params
    		
    		reac = reac + [reacts, prods, params]
    	
    		#print reac
        return reac