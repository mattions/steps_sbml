# -*- coding: utf-8 -*-

"""
 * Copyright (C) Thu Dec  4 09:28:29 GMT 2008 - Michele Mattioni:
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
from Input import *


class Experiment(object):
    
    def __init__(self, simulationManager):
        """Simulation Manager"""
        self.simMan = simulationManager
    
    """Create the inputs for the simulations with different type of setup"""
    def _orderInput(self, inputs):
        """
        Order the input to apply according to the sec of input.
        Return a dictionay of ordered input of the structure:
        timepoint --> list of input to apply in that inputTime
        :Parameters:
            inputs
                List of Input
        Return
            ordered dictionary 
        """
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
    
    
    
    def _createCalciumTrain(self, numSpikes, secOfInput, delay, quantity):
        """Create a train of Calcium spike
        :Parameters
            numSpikes: number of desired spikes
            secOfInput: initial spikes
            delay: dealy between the spikes
            quantity: how many ions"""
            
        inputCa = []
        for i in xrange(numSpikes):    
    
            inputTime = secOfInput * self.simMan.timePointIncrement
            input = Input(inputTime, 'Ca', quantity)
        
            inputCa.append(input)
        
            secOfInput += delay
        return inputCa
    
    
    def baseline(self):
        """Baseline. No input provided"""
        inputs = []
        return inputs
    
    def rig1(self):
        """Create the simulation as in Fernandez 2005
        
        http://view.ncbi.nlm.nih.gov/pubmed/17194217
        DARPP-32 is a robust integrator of dopamine and glutamate signals.
        PLoS Comput Biol, Vol. 2, No. 12. (22 December 2006)
        by E Fernandez, R Schiappa, JA Girault, N Le Novère
        
        """
        inputs = []
        inputcAMP = Input(100 * self.simMan.timePointIncrement , 'cAMP', 3975)
        inputCa = self._createCalciumTrain(numSpikes = 10, secOfInput = 150, 
                                           delay = 4, quantity = 2300)
        inputs = [inputcAMP]
        inputs.extend(inputCa)
        inputs = self._orderInput(inputs)
        return inputs
        
    def rig2(self):
        """
        Simulate the effect of a dopamine reward release just after a trains 
        of Glutamate release as suggested in Schultz 2002

        Getting formal with dopamine and reward.
        Neuron, Vol. 36, No. 2. (10 October 2002), pp. 241-263.
        by W Schultz
        http://view.ncbi.nlm.nih.gov/pubmed/12383780
        """
        inputs = []
        inputcAMP = Input(150 * self.simMan.timePointIncrement , 'cAMP', 3975)
        inputCa = self._createCalciumTrain(numSpikes = 10, secOfInput = 100, delay = 4, quantity = 2300)
        inputs = [inputcAMP]
        inputs.extend(inputCa)
        inputs = self._orderInput(inputs)
        return inputs
    
    def rig3(self):
        """
        Simulate the effect of a dopamine reward release just after a trains 
        of Glutamate release. The train of Glutamate is really fast (one spike every 4 ms)
        """
        inputs = []
        inputcAMP = Input(120 * self.simMan.timePointIncrement , 'cAMP', 3975)
        inputCa = self._createCalciumTrain(numSpikes = 10, secOfInput = 100, delay = 0.004, 
                                           quantity = 2300)
        inputs = [inputcAMP]
        inputs.extend(inputCa)
        inputs = self._orderInput(inputs)
        return inputs
    