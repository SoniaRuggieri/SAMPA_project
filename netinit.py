import netpyne
from netpyne import specs, sim 
import neuron 
import matplotlib 
import numpy as np
import random
# %matplotlib inline
from matplotlib import pyplot as plt
from netpyne.specs import Dict, netParams, simConfig
#%matplotlib inline

sim.create(netParams = netParams, simConfig = simConfig)

randsec=random.choice(np.array(list(sim.net.cells[0].secs.keys())))

#syn0 = neuron.h.SAMPAwt(sim.net.cells[0].secs[randsec]['hObj'](0.5))

syn=[]
for i in range(200):
  #syn0 = neuron.h.SAMPAwt(sim.net.cells[0].secs['dend10_20']['hObj'](0.5))
  syn0 =neuron.h.SAMPAwt(sim.net.cells[0].secs[randsec]['hObj'](0.5))
  syn0.gbarampa=42
  syn.append(syn0)
  #syn1 = neuron.h.SAMPAwt(sim.net.cells[0].secs['dendrite_1']['hObj'](0.5))
  #syn1.gbarampa=2000

for i in range(200):
  neuron.h.setpointer(sim.net.cells[1].secs['axon']['hObj'](0.5).rel._ref_T, 'glu', syn[i])
  #neuron.h.setpointer(sim.net.cells[1].secs['axon']['hObj'](0.5).rel._ref_T, glu', syn1)

#cellRule['secs']['dend10_20']['pointps']['SAMPAwt']['T'] = syn0.glu
#sim.net.cells[2].secs['axon']['hObj'](0.5).rel._ref_T=syn0.glu

#neuron.h.setpointer(sim.net.cells[3].secs['axon']['hObj'](0.5).rel._ref_T, 'glu', syn1)
#netParams.cellParams['rc']['secs']['dend10_20']['pointsps']={'mod':'SAMPAwt','loc':0.5}
#syn0.glu=1
sim.simulate()#netParams = netParams, simConfig = simConfig)
sim.analyze()