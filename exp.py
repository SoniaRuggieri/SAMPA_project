
  
from netpyne import specs, sim 
import matplotlib
import os
import json

# Network parameters
netParams = specs.NetParams()
syndist=0.560
somadist=0.560
somalength=3
diamsoma=somadist/2
diamsoma2=somadist*10
lpre=1
PREwt1={'secs':{}}
PREwt1['secs']['soma']={'geom':{}, 'mechs':{}}
PREwt1['secs']['soma']['geom']={'L': somadist*4,'diam':somadist/2,'nseg':11}
PREwt1['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['PREwt1']=PREwt1

PREwt={'secs':{}}
PREwt['secs']['soma']={'geom':{}, 'mechs':{}}
PREwt['secs']['soma']['geom']={'L': somadist*2,'diam':somadist,'nseg':11}
PREwt['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['PREwt']=PREwt

headpre={'secs':{}}
headpre['secs']['soma']={'geom':{}, 'mechs':{}}
headpre['secs']['soma']['geom']={'L':lpre,'diam':somadist,'nseg':1}
headpre['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['headpre']=headpre

head={'secs':{}}
head['secs']['soma']={'geom':{}, 'mechs':{}}
head['secs']['soma']['geom']={'L':lpre,'diam':somadist,'nseg':11}
head['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['head']=head 

somaWT={'secs':{}}
somaWT['secs']['soma']={'geom':{}, 'mechs':{}}
somaWT['secs']['soma']['geom']={'L':somadist*2,'diam':diamsoma2,'nseg':11}
somaWT['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['somaWT']=somaWT 

somaWT1={'secs':{}}
somaWT1['secs']['soma']={'geom':{}, 'mechs':{}}
somaWT1['secs']['soma']['geom']={'L':somadist*4,'diam':diamsoma,'nseg':11}
somaWT1['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['somaWT1']=somaWT1 

somaWTbig={'secs':{}}
somaWTbig['secs']['soma']={'geom':{}, 'mechs':{}}
somaWTbig['secs']['soma']['geom']={'L':somadist*10,'diam':diamsoma2,'nseg':11}
somaWTbig['secs']['soma']['mechs']['hh']={'gnabar': 0.12, 'gkbar':0.036, 'gl':0.003, 'el':-70}
netParams.cellParams['somaWTbig']=somaWTbig 

netParams.popParams['headpre_pop']={'cellType':'headpre','numCells':9}
netParams.popParams['PREwt1_pop']={'cellType':'PREwt1','numCells':3}
netParams.popParams['PREwt_pop']={'cellType':'PREwt','numCells':1}
netParams.popParams['head_pop']={'cellType':'head','numCells':9}
netParams.popParams['somaWT1_pop']={'cellType':'somaWT1','numCells':3}
netParams.popParams['somaWT_pop']={'cellType':'somaWT','numCells':1}
netParams.popParams['somaWTbig_pop']={'cellType':'somaWTbig','numCells':1}

simConfig = specs.SimConfig() 

simConfig.duration = 1*1e2         # Duration of the simulation, in ms
simConfig.dt = 0.025                # Internal integration timestep to use
simConfig.verbose = False           # Show detailed messages
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.recordStep = 0.1          # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'tut2'  # Set file output name
simConfig.savePickle = False        # Save params, network and sim output to pickle file
simConfig.saveJson = False

simConfig.analysis['plot2Dnet'] = {'showFig': True, 'saveFig':True} 
#simConfig.analysis['plotRaster'] = {'saveFig': True, 'syncLines': True}                  # Plot a raster
#simConfig.analysis['plotTraces'] = {'include': [1], 'saveFig': True}  # Plot recorded traces for this list of cells
#simConfig.analysis['plotRateSpectrogram'] = {'include': ['all']}
#simConfig.analysis['plotSpikeHist'] = {'include': ['S', 'I']}

sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)