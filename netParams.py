
from netpyne import specs, sim 
import neuron 
import matplotlib 
# %matplotlib inline
from matplotlib import pyplot as plt
from netpyne.specs import Dict


gl1=0.00005
netParams = specs.NetParams()

#has to be definied before importing the cells
netParams.popParams['rc_pop'] = {'cellType': 'relay', 'numCells': 1,'yRange': [0,5],'xRange': [0,5],'cellModel':'realrelay'}
netParams.popParams['ret_pop'] = {'cellType': 'RetGanCell', 'numCells': 1,'yRange': [6,10],'xRange': [6,10],'cellModel':'retgan'}

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
    cellRule['secs'][secName]['mechs']['pas'] = {'g': 1/5000, 'e': -70}
    cellRule['secs'][secName]['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.0005, 'el': -70}
    cellRule['secs'][secName]['geom']['cm'] = 1

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
RetGanCell['secs']['soma']['geom'] = {'diam': 2, 'L': 2, 'Ra': 123.0, 'cm':1 }  # soma geometry
RetGanCell['secs']['soma']['mechs']['pas'] = {'g': 1/5000, 'e': -70}
RetGanCell['secs']['soma']['mechs']['hh'] = { 'gnabar': 0.125, 'gkbar': 0.036, 'gl': gl1, 'el': -70}  # soma hh mechanism

RetGanCell['secs']['dend'] = {'geom': {}, 'topol': {}, 'mechs': {}}
RetGanCell['secs']['dend']['geom'] = {'diam': 2.0, 'L': 10.0, 'Ra': 123.0, 'cm': 1}
RetGanCell['secs']['dend']['topol'] = {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0}
RetGanCell['secs']['dend']['mechs']['pas'] = {'g': 1/5000, 'e': -70}
RetGanCell['secs']['dend']['mechs']['hh'] = { 'gnabar': 0.125, 'gkbar': 0.036, 'gl': gl1, 'el': -70}  # soma hh mechanism

RetGanCell['secs']['axon'] = {'geom': {}, 'topol': {}, 'mechs': {}}
RetGanCell['secs']['axon']['geom'] = {'diam': 2.0, 'L': 10.0, 'Ra': 123.0, 'cm': 1}
RetGanCell['secs']['axon']['topol'] = {'parentSec': 'soma', 'parentX': 0.0, 'childX': 0}
RetGanCell['secs']['axon']['mechs']['pas'] = {'g': 1/5000, 'e': -70}
RetGanCell['secs']['axon']['mechs']['hh'] = { 'gnabar': 0.125, 'gkbar': 0.036, 'gl': gl1, 'el': -70}  # soma hh mechanism
RetGanCell['secs']['axon']['mechs']['caL']={'p':0.0002,'q':10}
RetGanCell['secs']['axon']['mechs']['rel']={'Ves': 0.1, 'Fmax' : 0.001,'b': 1e16 ,'u':0.1,'k1':1000,
                                            'k2':0.1,'k3':4,'nt':10000,'kh':10,'kd':5e-5,'kt':1e-3,'depth':1,'taur':1e10}

netParams.cellParams['RetGanCell'] = RetGanCell   


## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {
    'mod': 'Exp2Syn', 
    'tau1': 0.5, 
    'tau2': 3.0, 
    'e': 0}  # excitatory synaptic mechanism

netParams.stimSourceParams['bkg'] = {
    'type': 'NetStim',
    'interval': 50,
    'number': 5, 
    'start': 0, 
    'noise': 0
}

netParams.stimTargetParams['bkg->ret_pop'] = {
    'source': 'bkg', 
    'conds': {'pop': 'ret_pop','cellType':'RetGanCell'}, 
    'weight': 0.005, 
    'delay': 0, 
    'sec': 'dend',
    'loc': 0,
    'synMech': 'exc'}



simConfig = specs.SimConfig() 

simConfig.duration = 1*1e2         # Duration of the simulation, in ms
simConfig.dt = 0.025                # Internal integration timestep to use
simConfig.verbose = False  

#simConfig.recordCells = ['ret_pop']      # Show detailed messages
#simConfig.recordTraces['soma_voltage'] = {'sec':'axon','loc':0.5,'var':'v'}
#simConfig.recordCells = ['ret_pop'] 
simConfig.recordTraces['T_rel'] = {'sec':'axon','loc':0.5,'var':'T_rel'}  # Dict with traces to record
#simConfig.recordCells = ['rc_pop'] 
simConfig.recordTraces['soma_V'] = {'sec':'soma','loc':0.5,'var':'v'}  # Dict with traces to record

simConfig.recordStep = 0.1          # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'SAMPA'  # Set file output name
simConfig.savePickle = False        # Save params, network and sim output to pickle file
simConfig.saveJson = False

simConfig.analysis['plot2Dnet'] = {'showFig': True}#, 'saveFig':True} 
simConfig.analysis['plotRaster'] = {'showFig': True, 'syncLines': True}                  # Plot a raster
simConfig.analysis['plotTraces'] = {'showFig': True,'include': ['ret_pop','rc_pop'] }  # Plot recorded traces for this list of cells
#simConfig.analysis['plotRateSpectrogram'] = {'showFig': True,'include': ['all']}
#simConfig.analysis['plotSpikeHist'] = {'showFig': True,'include': ['ret']}

sim.create(netParams = netParams, simConfig = simConfig)
