import threading
import io
import numpy

class Iteration(threading.Thread):
    
    def __init__ (self, sim, tStart, tStop, inputs, species, tpnt, nTPoints,
                  legendDict, dt_exp, currentDir, it):
        self.sim = sim
        self.tStart = tStart
        self.tStop = tStop
        self.inputs = inputs
        self.species = species
        self.tpnt = tpnt
        self.nTPoints = nTPoints
        self.legendDict = legendDict
        self.dt_exp = dt_exp
        self.currentDir = currentDir
        self.resName = "res_" + str(it)
        threading.Thread.__init__ ( self )

    def orderInput(self, inputs):
                # Ordering the input
        inputToApply = {}
        
        for input in (inputs):
            timePoint = input.getInputTimePoint()
            if (timePoint in inputToApply):
                list = inputToApply[timePoint] # Grabbing all the present Inputs
                list.append(input) # adding the inputs
                inputToApply[timePoint] = list # Update
            else:
                inputToApply[timePoint] = [input]        
        return inputToApply
    
    def instantSec(self, t):
        if (t % (pow(10, abs(self.dt_exp))) == 0):
            instantSec = t / pow(10, abs(self.dt_exp))
            print "iteration %s sec %f" %(self.resName, instantSec)
    
    def runTime(self, inputToApply):
        """
            Function to run the simulation from one point to another one
            :params:
                sim
                    The simulator variable of STEPS
                tp1
                    Time point where to start the simulation (ex.: 0)
                tp2
                    Time where to stop the simulation (ex.: 3001)
        """
#        print inputToApply
        res = numpy.zeros([self.nTPoints, len(self.species)])
        for t in xrange(self.tStart, self.tStop):
            if (inputToApply is not None and t in inputToApply):
                inputList = inputToApply.pop(t)
                for inp in inputList:
                     print inp, t
                     mol = inp.getMol()
                     q = inp.getQuantity()
                     self.sim.setCompCount('comp', mol, 
                                      self.sim.getCompCount('comp', mol) + q)
            i = 0 
            for specie in self.species:
                res[t,i] = self.sim.getCompCount('comp', specie)
                self.legendDict[specie] = i
                i = i + 1
            self.sim.run(self.tpnt[t])
            self.instantSec(t)
        return res
    
    def run (self):
                # We need to reset the simulator
        self.sim.reset()        
        
        # Setting the conc
        for specie in self.species:
            self.sim.setCompConc('comp', specie, self.species[specie])
        
        # Ordering the input
        inputToApply = self.orderInput(self.inputs)
        
        res = self.runTime(inputToApply)
        #Save the result
            
        io.loader.saveRes(self.currentDir, res, self.resName)
        