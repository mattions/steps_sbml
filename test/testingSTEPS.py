from pylab import *
import numpy 

def create_graph(res, tpnt, tit):
   figure()
   plot(tpnt, res[:,0])
   plot(tpnt, res[:,1])
   plot(tpnt, res[:,2])
   xlabel('Time (sec)')
   ylabel('#molecules')
   legend(('A','B','C'))
   title (tit)
   show()

# Setting the kinetic simulation
import steps.model as smodel
mdl = smodel.Model()
molA = smodel.Spec('molA', mdl)
molB = smodel.Spec('molB', mdl)
molC = smodel.Spec('molC', mdl)
volsys = smodel.Volsys('vsys', mdl)
lhsTest = [molA,molB]
rhsTest = [molC]
print 'kreac_f', volsys, lhsTest, rhsTest 
kreac_f = smodel.Reac('kreac_f', volsys, lhs=lhsTest, rhs=rhsTest)



kreac_f.kcst = 0.3e6
kreac_b = smodel.Reac('kreac_b', volsys, \
    lhs=[molC], rhs=[molA,molB])
kreac_b.kcst = 0.7

#setting the geometry
import steps.geom.wm as swm
mesh = swm.Geom()
comp = swm.Comp('comp', mesh)
comp.addVolsys('vsys')
comp.vol = 1.6667e-21


import steps.rng as srng
r = srng.create('mt19937', 512)
r.initialize(23412)

import steps.wmdirect as swmdirect

sim = swmdirect.Solver(mdl, mesh, r)

#Setting the conc
sim.reset()
sim.setCompConc('comp', 'molA', 31.4e-6)
sim.setCompConc('comp', 'molB', 22.3e-6)


tpnt = numpy.arange(0.0, 2.001, 0.001)
res = numpy.zeros([2001,3])

for t in xrange(0,2001):
    sim.run(tpnt[t])
    res[t,0] = sim.getCompCount('comp', 'molA')
    res[t,1] = sim.getCompCount('comp', 'molB')
    res[t,2] = sim.getCompCount('comp', 'molC')



create_graph(res, tpnt, "single iteration")

res = numpy.zeros([100,2001,3])#iteration, timepoints, 
tpnt = numpy.arange(0.0, 2.001, 0.001)
n_it = 100

print "Performing %d iterations." %n_it


for i in xrange(0, n_it):
    sim.reset()
    sim.setCompConc('comp', 'molA', 31.4e-6)
    sim.setCompConc('comp', 'molB', 22.3e-6)
    
    for t in xrange(0,2001):
        sim.run(tpnt[t])
        res[i,t,0] = sim.getCompCount('comp', 'molA')
        res[i,t,1] = sim.getCompCount('comp', 'molB')
        res[i,t,2] = sim.getCompCount('comp', 'molC')

res2 = numpy.mean(res, 0)
create_graph(res2, tpnt, "%d iterations." %n_it)



######################
## Adding 10 molecules
for i in xrange(0, n_it):

   # Resetting the simulator
   sim.reset()
   sim.setCompConc('comp', 'molA', 31.4e-6)
   sim.setCompConc('comp', 'molB', 22.3e-6)

   for t in xrange(0,1001):
         sim.run(tpnt[t])
         res[i,t,0] = sim.getCompCount('comp', 'molA')
         res[i,t,1] = sim.getCompCount('comp', 'molB')
         res[i,t,2] = sim.getCompCount('comp', 'molC')
   # Add 10 molecules of species A
   sim.setCompCount('comp', 'molA', sim.getCompCount('comp', 'molA') + 10)
   for t in xrange(1001,2001):
         sim.run(tpnt[t])
         res[i,t,0] = sim.getCompCount('comp', 'molA')
         res[i,t,1] = sim.getCompCount('comp', 'molB')
         res[i,t,2] = sim.getCompCount('comp', 'molC')

res3 = numpy.mean(res, 0)

create_graph(res3, tpnt, "%d iterations." %n_it + " Added 10 A molecules")

# clamped

for i in xrange(0, n_it):

   # Resetting the simulator
   sim.reset()
   sim.setCompConc('comp', 'molA', 31.4e-6)
   sim.setCompConc('comp', 'molB', 22.3e-6)
   for t in xrange(0,101):
       sim.run(tpnt[t])
       res[i,t,0] = sim.getCompCount('comp', 'molA')
       res[i,t,1] = sim.getCompCount('comp', 'molB')
       res[i,t,2] = sim.getCompCount('comp', 'molC')
   sim.setCompClamped('comp', 'molA', True)
   for t in xrange(101,601):
       sim.run(tpnt[t])
       res[i,t,0] = sim.getCompCount('comp', 'molA')
       res[i,t,1] = sim.getCompCount('comp', 'molB')
       res[i,t,2] = sim.getCompCount('comp', 'molC')
   sim.setCompClamped('comp', 'molA', False)
   for t in xrange(601,2001):
       sim.run(tpnt[t])
       res[i,t,0] = sim.getCompCount('comp', 'molA')
       res[i,t,1] = sim.getCompCount('comp', 'molB')
       res[i,t,2] = sim.getCompCount('comp', 'molC')


res3 = numpy.mean(res, 0)
create_graph(res3, tpnt, "Mol A clamped (buffered)")
   

### Experimenting the channel

def run(i, tp1, tp2):
    for t in xrange(tp1,tp2):
        sim.run(tpnt[t])
        res[i,t,0] = sim.getCompCount('comp', 'molA')
        res[i,t,1] = sim.getCompCount('comp', 'molB')
        res[i,t,2] = sim.getCompCount('comp', 'molC')



# Resetting the simulator
res = numpy.zeros([100,12001,3])
tpnt = numpy.arange(0.0, 12.001, 0.001)



for i in xrange (0, 100):
   sim.reset()
   sim.setCompConc('comp', 'molA', 31.4e-6)
   sim.setCompConc('comp', 'molB', 22.3e-6)
   sim.setCompReacActive('comp', 'kreac_f', False)
   run(i,0,2001)
   sim.setCompReacActive('comp', 'kreac_f', False)
   run(i,2001,4001)
   sim.setCompReacActive('comp', 'kreac_f', True)
   run(i,4001,6001)
   sim.setCompReacActive('comp', 'kreac_b', False)
   run(i,6001,8001)
   sim.setCompReacActive('comp', 'kreac_b', True)
   run(i,8001,10001)
   sim.setCompReacActive('comp', 'kreac_f', False)
   sim.setCompReacActive('comp', 'kreac_b', False)
   run(i,10001,12001)

res4 = numpy.mean(res, 0)
create_graph(res4, tpnt, "Testing the inactivating \
   of the channel (the reaction)")



