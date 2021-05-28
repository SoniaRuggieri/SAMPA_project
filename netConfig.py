from netpyne import specs, sim 
import neuron 
import matplotlib 
import numpy as np
import random
# %matplotlib inline
from matplotlib import pyplot as plt
from netpyne.specs import Dict
%matplotlib inline

simConfig = specs.SimConfig() 

simConfig.duration = 4*1e2         # Duration of the simulation, in ms
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