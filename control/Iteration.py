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

import threading
import io
import numpy

class Iteration(threading.Thread):
    
    def __init__ (self, sim, tStart, tStop, inputs, species, tpnt, nTPoints,
                  legendDict, dt_exp, currentDir, it, interval):
        self.sim = sim
        self.tStart = tStart
        self.tStop = tStop
        self.inputs = inputs
        self.species = species
        self.tpnt = tpnt
        self.nTPoints = nTPoints
        self.legendDict = legendDict
        self.dt_exp = dt_exp
        self.timePointIncrement = pow(10, abs(dt_exp))
        self.currentDir = currentDir
        self.resName = "res_" + str(it)
        self.interval = interval
        threading.Thread.__init__ ( self )

    
    def instantSec(self, t):
        """
        Report the status of the simulation according to the interval
        :Params:
            t 
                The timepoint
        """
        instantSec = t / self.timePointIncrement
        if (t % (self.interval * self.timePointIncrement) == 0):
            
            print "iteration %s sec %f" %(self.resName, instantSec)
##        else:
##            print "iteration %s sec %f" %(self.resName, instantSec)
    
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
                     mol = inp.getMol()
                     q = inp.getQuantity()
#                     print "Input applied: Mol %s, Quantity %e, time %d" %(mol, q, t) 
                     self.sim.setCompCount('comp', mol, 
                                      self.sim.getCompCount('comp', mol) + q)
            i = 0 
            for specie in self.species:
                res[t,i] = self.sim.getCompCount('comp', specie)
                self.legendDict[specie] = i
                i = i + 1
            self.sim.run(self.tpnt[t])
            self.instantSec(t)
            #print t, self.tStart, self.tStop

        return res
    
    def run (self):
                # We need to reset the simulator
        self.sim.reset()        
        
        # Setting the conc
        for specie in self.species:
            self.sim.setCompConc('comp', specie, self.species[specie])
        
        res = self.runTime(self.inputs)
        
        #Save the result
        io.loader.saveRes(self.currentDir, res, self.resName)
        