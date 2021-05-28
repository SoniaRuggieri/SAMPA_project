import netpyne
from netpyne import specs, sim 
import neuron 
import matplotlib 
import numpy as np
import random
# %matplotlib inline
from matplotlib import pyplot as plt
from netpyne.specs import Dict
netParams = specs.NetParams()

gl1=1/5000
#has to be definied before importing the cells
netParams.popParams['rc_pop'] = {'cellType': 'relay', 'numCells': 1,'yRange': [0,5],'xRange': [0,5],'cellModel':'realrelay'}
netParams.popParams['ret_pop'] = {'cellType': 'RetGanCell', 'numCells': 2,'yRange': [6,10],'xRange': [6,10],'cellModel':'retgan'}

### HH3D HOC
# cellRule = netParams.importCellParams(
#     label='relay_pyr', 
#     fileName='geom_pyr.hoc', 
#     cellName='relay', 
#     importSynMechs=False,
#     )
cellRule = netParams.importCellParams(
    label='relay_pyr', 
    fileName='relayCell.py', 
    cellName='relay', 
    conds = {'cellType' : 'relay', 'cellModel' : 'realrelay'},
    importSynMechs=False,
    )

for secName in cellRule['secs']:
    #cellRule['secs'][secName]['mechs']['pas'] = {'g': 1/30000, 'e': -70}
    cellRule['secs'][secName]['mechs']['hh'] = {'gnabar': 0.022, 'gkbar': 0.0008, 'gl': 1/30000, 'el': -70}
    cellRule['secs'][secName]['geom']['cm'] = 2
    cellRule['secs'][secName]['vinit']=-70
    cellRule['secs'][secName]['geom']['Ra']=70
    cellRule['secs'][secName]['ions'] = {'k': {'e': -90.0}, 'na': {'e': 55.0}}

'''
cellRule = netParams.importCellParams(
    label='rc', 
    fileName='relaymorph.hoc', 
    cellName='relay',
    importSynMechs=False,
    conds={'cellType': 'relay','cellModel': 'realrelay'}
    )'''

# netParams.cellParams['relay_pyr'] = cellRule

RetGanCell = {'secs': {}}
RetGanCell['secs']['soma'] = {'geom': {}, 'mechs': {}}
RetGanCell['secs']['soma']['geom'] = {'diam': 1, 'L': 2, 'Ra': 123.0, 'cm':1 }  # soma geometry
RetGanCell['secs']['soma']['mechs']['hh'] = { 'gnabar': 0.125, 'gkbar': 0.025, 'gl': gl1, 'el': -70}  # soma hh mechanism
RetGanCell['secs']['soma']['ions'] = {'k': {'e': -90.0}, 'na': {'e': 55.0}}
RetGanCell['secs']['dend'] = {'geom': {}, 'topol': {}, 'mechs': {}}

RetGanCell['secs']['dend']['geom'] = {'diam': 1.0, 'L': 10.0, 'Ra': 123.0, 'cm': 1}
RetGanCell['secs']['dend']['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}
RetGanCell['secs']['dend']['mechs']['hh'] = { 'gnabar': 0.125, 'gkbar': 0.025, 'gl': gl1, 'el': -70}  # soma hh mechanism
RetGanCell['secs']['dend']['ions'] = {'k': {'e': -90.0}, 'na': {'e': 55.0}}

RetGanCell['secs']['axon'] = {'geom': {}, 'topol': {}, 'mechs': {}}
RetGanCell['secs']['axon']['geom'] = {'diam': 1.0, 'L': 10.0, 'Ra': 123.0, 'cm': 1}
RetGanCell['secs']['axon']['topol'] = {'parentSec': 'soma', 'parentX': 0.0, 'childX': 0}
RetGanCell['secs']['axon']['mechs']['hh'] = { 'gnabar': 0.125, 'gkbar': 0.025, 'gl': gl1, 'el': -70}  # soma hh mechanism
RetGanCell['secs']['axon']['mechs']['caL']={'p':0.0002,'q':10}
RetGanCell['secs']['axon']['mechs']['rel']={'Ves': 0.1, 'Fmax' : 0.001,'b': 1e16 ,'u':0.1,'k1':1000,
                                            'k2':0.1,'k3':4,'nt':10000,'kh':10,'kd':5e-5,'kt':1e-3,'depth':1,'taur':1e10}
RetGanCell['secs']['axon']['ions'] = {'k': {'e': -90.0}, 'na': {'e': 55.0}}
netParams.cellParams['RetGanCell'] = RetGanCell   




## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {
    'mod': 'Exp2Syn', 
    'tau1': 0.5, 
    'tau2': 3.0, 
    'e': 0}  # excitatory synaptic mechanism

netParams.stimSourceParams['bkg'] = {
    'type': 'NetStim',
    'interval': 30,
    'number': 5, 
    'start': 50, 
    'noise': 0
}

netParams.stimTargetParams['bkg->ret_pop'] = {
    'source': 'bkg', 
    'conds': {'pop': 'ret_pop','cellType':'RetGanCell'}, 
    'weight': 0.008, 
    'delay': 0, 
    'sec': 'dend',
    'loc': 0,
    'synMech': 'exc'}


