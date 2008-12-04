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

import numpy
import io
from Input import *
from Iteration import *
import os
import thread
import copy

class SimulationManager(object):
	"""
		Define a set of ready to use Simulations
	"""
	

	
	def __init__(self, nSec, dt_exp, species, iterations, currentDir, interval):
		"""
			Constructor for the Simulation Manager
			:Parameters
				nSec: Number of Seconds to simulate
				dt_exp:	Exponential used to store the data to the array
				species: Species in the simulation
				iterations: number of iterations the simulation should be run
				currentDir: Directory where the Simulation will be saved
				interval: Interval of sec between the log
		"""	
		self.nSec = nSec
		self.dt = pow(10, dt_exp)
		self.dt_exp = dt_exp
		self.lastTPoint = nSec + self.dt #Extreme of the array
		self.tpnt = numpy.arange(0.0, self.lastTPoint, self.dt) # Numpy array, with start, end and increment
		self.timePointIncrement = pow(10, abs(dt_exp))
		self.nTPoints = nSec * self.timePointIncrement + 1 # Number of Time Points
		self.species = species
		self.numMol = len(species)
		self.iterations = iterations # Number iterations
		self.createRes(iterations)
#		self.res = numpy.zeros([self.__iterations, self.nTPoints, self.numMol])
		self.legendDict = {} # Map the Id of the specie with the number
		self.currentDir = currentDir
		self.interval = interval

		
	def createRes(self, iterations):
		"""
		Create the array where to store the result of the simulation
		"""
		for i in xrange (iterations):
			resName = "res_" + str(i) 
			self.resName = numpy.zeros([self.nTPoints, self.numMol])
	
	def inputsIn(self, sim, inputs, it):
		"""
		Create an iteration thread
		:params:
			sim 
				The simulation object of STEPS
			inputs
				List of Inputs to give during the simulation
		"""
			
		iter = Iteration(sim, 0, self.nTPoints, inputs, self.species, self.tpnt, self.nTPoints,
				  self.legendDict, self.dt_exp, self.currentDir, it, self.interval)
		return iter