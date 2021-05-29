# import sys
# # sys.path.insert(0, '../../my_netpyne/')
# sys.path.insert(0, '/home/craig/netpyne/')

from netpyne import specs, sim 

import neuron 
import matplotlib 
import numpy as np
import random
# %matplotlib inline
from matplotlib import pyplot as plt
from netpyne.specs import Dict


##separate and put at the beginning
simConfig = specs.SimConfig() 

simConfig.duration = 4*1e2         # Duration of the simulation, in ms
simConfig.dt = 0.1              # Internal integration timestep to use
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
simConfig.analysis['plotTraces'] = {'showFig': True,'include': ['ret_pop','rc_pop'] } 
simConfig.analysis['plotRxDConcentration'] = {'speciesLabel': 'xwt', 'regionLabel': 'ecs'}
#simConfig.analysis['plotCSD'] = {'timeRange': [10,45]} # Plot recorded traces for this list of cells
#simConfig.analysis['plotRateSpectrogram'] = {'showFig': True,'include': ['all']}
#simConfig.analysis['plotSpikeHist'] = {'showFig': True,'include': ['ret']}


gl1=1/5000
netParams = specs.NetParams()

netParams.sizeX = 200
netParams.sizeY = 200
netParams.sizeZ = 200 

#has to be definied before importing the cells
netParams.popParams['rc_pop'] = {'cellType': 'relay', 'numCells': 1,'yRange': [0,5],'xRange': [0,5],'cellModel':'realrelay'}
netParams.popParams['ret_pop'] = {'cellType': 'RetGanCell', 'numCells': 2,'yRange': [6,10],'xRange': [6,10],'cellModel':'retgan'}

cellRule = netParams.importCellParams(
    label='relay_pyr', 
     fileName='geom_pyr.hoc', 
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

netParams.addCellParamsSecList(label='relay_pyr', secListName='proximal', somaDist=[0, 100])  # sections within 50 um of soma

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
RetGanCell['secs']['axon']['mechs']['sumpwt']={'imaxwt':1}
#here I neede do include a pump in order to convert the range variable from rel (T_rel, glutamate produced internally) to a current. This because the species in the rxd has to refer to an ion, otherwise it doesn't work

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

regions={}
regions['ecs'] ={'extracellular': True, 'xlo': -100, 'ylo': -100, 'zlo': -100, 'xhi': 100, 'yhi': 100, 'zhi': 100, 'dx': 10, 'volume_fraction': 0.2, 'tortuosity': 1.6}
regions['mem'] = {'cells' : 'all', 'secs' : 'all', 'nrn_region' : None, 'geometry' : 'membrane'}
regions['cyt'] = {'cells': 'all',  'secs':'all','nrn_region': 'i'}#,'geometry': {'class': 'FractionalVolume', 'args': { 'surface_fraction': 1}}}}==
netParams.rxdParams['regions'] = regions

species={}
species['xwt']= {'regions' : ['ecs','cyt', 'mem'], 'name' : 'xwt', 'd' : 1}
netParams.rxdParams['species'] =species

netParams.rxdParams['multicompartmentReactions'] = {'someReaction' : {'reactant': 'xwt[cyt]', 'product': 'xwt[ecs]', 'rate_f': 1, 'membrane' : 'mem', 'custom_dynamics':'True'}} #, 'membrane': 'cyt_er_membrane'

sim.initialize(netParams = netParams, simConfig = simConfig)  # create network object and set cfg and net params
sim.net.createPops()                  # instantiate network populations
sim.net.createCells()                 # instantiate network cells based on defined populations
sim.net.connectCells()                # create connections between cells based on params
sim.net.addStims()            # setup variables to record for each cell (spikes, V traces, etc)
sim.net.addRxD(nthreads=4)  
sim.simulate()
sim.analyze()      
