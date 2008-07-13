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
		Simulate creating one iteration thread for the number of the iteration
		:params:
			sim 
				The simulation object of STEPS
			inputs
				List of Inputs to give during the simulation
		"""
			
		iter = Iteration(sim, 0, self.nTPoints, inputs, self.species, self.tpnt, self.nTPoints,
				  self.legendDict, self.dt_exp, self.currentDir, it, self.interval)
		return iter