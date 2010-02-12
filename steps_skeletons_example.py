NITER = 10
ENDTIME = 0.501
DT = 0.001
POINTS = int(ENDTIME/DT)
KCST = 10.0e6
ACOUNT = 100
BCOUNT = 200
CCOUNT = 0
COMPVOL = 1.0e-18

import steps.model as smodel
import steps.geom as swm
import steps.rng as srng
import steps.solver as ssolver

mdl = smodel.Model()


#################################
# SBML swap

A = smodel.Spec('A', mdl)				
B = smodel.Spec('B', mdl)
C = smodel.Spec('C', mdl)

volsys = smodel.Volsys('vsys', mdl)
reac = smodel.Reac('reac', volsys, lhs=[A,B], rhs = [C], kcst = KCST)

mesh = swm.Geom()

# Create the cytosol compartment
comp = swm.Comp('comp', mesh, vol = COMPVOL)					
comp.addVolsys('vsys')


############################


r = srng.create('mt19937', 256)
r.initialize(7233)

sim = ssolver.Wmdirect(mdl, mesh, r)
from pylab import *

import numpy
tpnt = numpy.arange(0.0, ENDTIME, DT)
res_m = numpy.zeros([NITER, POINTS, 3])

for i in xrange (0, NITER):
	sim.reset()
	sim.setCompCount('comp', 'A', ACOUNT)               
	sim.setCompCount('comp', 'B', BCOUNT)  
	sim.setCompCount('comp', 'C', CCOUNT)                   	
	for t in xrange(0,POINTS):
		sim.run(tpnt[t])
		res_m[i,t,0] = sim.getCompCount('comp', 'A')
		res_m[i,t,1] = sim.getCompCount('comp', 'B')		
		res_m[i,t,2] = sim.getCompCount('comp', 'C')		

mean_res = numpy.mean(res_m, 0)

plot(tpnt, mean_res[:,0], label = 'A')
plot(tpnt, mean_res[:,1], label = 'B')
plot(tpnt, mean_res[:,2], label = 'C')

xlabel('Time (sec)')
title('%d iterations' %NITER)
legend()
show()

