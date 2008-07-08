import io
from libsbml import *

reader = SBMLReader()
document = reader.readSBML("BIOMD0000000152.xml")
model = document.getModel()


ListOfComp = model.getListOfCompartments()
# getting the volume of the compartment
print "main -- model %s\tList %s" %( model, ListOfComp)
volComp = 0
for com in ListOfComp:
    volComp = com.getVolume()
    print volComp

print "Main Loop -- Vol of the comp %e" %volComp



iSbml = io.sbmlImporter("BIOMD0000000152.xml")

model  = iSbml.getModel()

#ListOfComp = model.getListOfCompartments()
#print "module -- model %s\tList %s" %( model, ListOfComp)
## getting the volume of the compartment
#volComp = 0
#for com in ListOfComp:
#    volComp = com.getVolume()

volCompMod = iSbml.getVolume()

print "Module Loop -- Vol of the comp %e" %volCompMod