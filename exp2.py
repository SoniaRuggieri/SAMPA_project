
  
from netpyne import specs, sim 
import matplotlib
import os
import json
### HH3D SWC
netParams = specs.NetParams()
cellRule = netParams.importCellParams(
    label='rc', 
    fileName='relaymorph.hoc', 
    cellName='relay',
    importSynMechs=False,
    )
# Network parameters

cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}
for secName in cellRule['secs']:
    cellRule['secs'][secName]['mechs']['pas'] = {'g': 0.0000357, 'e': -70}
    cellRule['secs'][secName]['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}
    cellRule['secs'][secName]['geom']['cm'] = 1


RetGanCell = {'secs': {}}
RetGanCell['secs']['soma'] = {'geom': {}, 'mechs': {}}
RetGanCell['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0}  # soma geometry
RetGanCell['secs']['soma']['mechs']['hh'] = { 'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}  # soma hh mechanism
netParams.cellParams['RetGanCell'] = RetGanCell


cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}
for secName in cellRule['secs']:
    cellRule['secs'][secName]['mechs']['pas'] = {'g': 0.0000357, 'e': -70}
    cellRule['secs'][secName]['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}
    cellRule['secs'][secName]['geom']['cm'] = 1


## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {
    'mod': 'Exp2Syn', 
    'tau1': 0.1, 
    'tau2': 5.0, 
    'e': 0}  # excitatory synaptic mechanism

netParams.stimSourceParams['bkg'] = {
    'type': 'NetStim', 
    'rate': 50, 
    'noise': 0.5}


netParams.stimTargetParams['bkg->ret'] = {
    'source': 'bkg', 
    'conds': {'pop': 'S'}, 
    'weight': 0.01, 
    'delay': 5, 
    'synMech': 'exc'}


netParams.popParams['rc_pop'] = {'cellType': 'relay', 'numCells': 2}
netParams.popParams['ret_pop'] = {'cellType': 'relay', 'numCells': 2}

simConfig = specs.SimConfig() 

simConfig.duration = 1*1e2         # Duration of the simulation, in ms
simConfig.dt = 0.025                # Internal integration timestep to use
simConfig.verbose = False           # Show detailed messages
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.recordStep = 0.1          # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'tut2'  # Set file output name
simConfig.savePickle = False        # Save params, network and sim output to pickle file
simConfig.saveJson = False

#simConfig.analysis['plot2Dnet'] = {'showFig': True, 'saveFig':True} 
simConfig.analysis['plotRaster'] = {'saveFig': True}#, 'syncLines': True}                  # Plot a raster
#simConfig.analysis['plotTraces'] = {'include': [1], 'saveFig': True}  # Plot recorded traces for this list of cells
#simConfig.analysis['plotRateSpectrogram'] = {'include': ['all']}
#simConfig.analysis['plotSpikeHist'] = {'include': ['S', 'I']}

sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)