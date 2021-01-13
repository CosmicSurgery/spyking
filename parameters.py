'''


'''

import numpy as np
import pandas as pd
import random



### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
rs = {}
fs = {}
lts = {}
ib = {}


'''
SYNAPSE PARAMETERS
keys:
    >input_neuron_cell_type
        >conduction_delay
        >output_neuron_cell_type
            >Ts - slow time delay
            >Tf - fast time delay
            >Rs - slow rise potential
            >Rf - fast rise potential
'''
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

### REGULAR ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
# regular spiking
key='rs'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
rs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# fast spiking
key='fs'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
rs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# low threshold spiking
key='lts'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
rs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# intrinsic burst
key='ib'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
rs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### FAST SPIKING ###

# regular spiking
key='rs'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
fs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# fast spiking
key='fs'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
fs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# low threshold spiking
key='lts'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
fs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# intrinsic burst
key='ib'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
fs[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### LOW THRESHOLD ###

# regular spiking
key='rs'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
lts[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# fast spiking
key='fs'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
lts[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# low threshold spiking
key='lts'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
lts[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# intrinsic burst
key='ib'
Ts = 31/32
Tf = 7/8
Rs = -5
Rf = -5
lts[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### INTRINSIC BURST ###

# regular spiking
key='rs'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
ib[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# fast spiking
key='fs'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
ib[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# low threshold spiking
key='lts'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
ib[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})
# intrinsic burst
key='ib'
Ts = 31/32
Tf = 7/8
Rs = 5
Rf = 5
ib[key] = pd.Series({'Ts':Ts, 'Tf':Tf, 'Rs':Rs, 'Rf':Rf})

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
delay_matrix = {}
density_matrix={}
neuron_radius={}
color = {}
connectivity_distance = {} #Probability of a synapse forming as a function of distance from 0 to 1 units
connectivity_cell_type = {} #Probability of a synapse forming as a function of cell_type
a, b, c, d, v, u ,I = {}, {}, {}, {}, {}, {}, {}
#connectivity_distance definitions
small = 12
medium = 10
large = 8
x= np.arange(0,1,0.001)
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
# Regular Spiking - Pyramidal

key='rs'
conduction_delay=3.5 / 1000
delay_matrix[key] = conduction_delay
density=80
density_matrix[key] = density
neuron_radius[key] = 50 / 1000
color[key] = 'dodgerblue'
connectivity_distance[key] = [np.e**(-small*i) for i in x]
connectivity_cell_type[key] = pd.Series({
     'rs' : 0.8, 'fs' : 0.8, 'lts' : 0.8, 'ib' : 0.8
})
a[key], b[key], c[key], d[key], v[key], I[key] = 0.02,0.2,-65,8, -65, [0]
u[key] = v[key]*b[key]
# Fast Spiking - Parvalbumin
key='fs'
conduction_delay=1 / 1000
delay_matrix[key] = conduction_delay
density=10
density_matrix[key] = density
neuron_radius[key] = 50 / 1000
color[key] = 'firebrick'
connectivity_distance[key] = [np.e**(-large*i) for i in x]
connectivity_cell_type[key] = pd.Series({
     'rs' : 0.8, 'fs' : 0.8, 'lts' : 0.0, 'ib' : 0.0
     })
a[key], b[key], c[key], d[key], v[key], I[key] = 0.02,0.25,-65,2, -65, [0]
u[key] = v[key]*b[key]
# Low Threshold Spiking - Somatostatin
key='lts'
conduction_delay=3.5 / 1000
delay_matrix[key] = conduction_delay
density=6
density_matrix[key] = density
neuron_radius[key] = 50 / 1000
color[key] = 'forestgreen'
connectivity_distance[key] = [np.e**(-large*i) for i in x]
connectivity_cell_type[key] = pd.Series({
     'rs' : 0.8, 'fs' : 0.8, 'lts' : 0.0, 'ib' : 0.0
     })
a[key], b[key], c[key], d[key], v[key], I[key] = 0.1,0.2,-65,2, -65, [0]
u[key] = v[key]*b[key]
# Intrinsic Burst - VIP

key='ib'
conduction_delay=3.5 / 1000
delay_matrix[key] = conduction_delay
density=4
density_matrix[key] = density

neuron_radius[key] = 50 / 1000
color[key] = 'yellow'
connectivity_distance[key] = [np.e**(-large*i) for i in x]
connectivity_cell_type[key] = pd.Series({
     'rs' : 0.0, 'fs' : 0.3, 'lts' : 0.8, 'ib' : 0.0
     })
a[key], b[key], c[key], d[key], v[key], I[key] = 0.02,0.2,-55,4, -65, [0]
u[key] = v[key]*b[key]
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
density_matrix = pd.Series(density_matrix)
delay_matrix = pd.Series(delay_matrix)
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
'''
NETWORK LEVEL PARAMETERS
keys:
    >network
        >timing - T1, T2, step, sampling rate 
'''
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
network = {}

# Default timing parameters

key = 'timing'

T1 = 0
T2 = 1000 # milliseconds
h = 0.1
sf = 10000 # Hz

network[key] = pd.Series({'T1':T1, 'T2':T2, 'h':h, 'sf':sf})

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
'''
External Input parameters
keys:
    >task
        >fmax
        >f
        >task_x
        >task_y
        >task_z
        >dmax = np.linalg.norm(np.array(task_x,task_y,task_z) - np.array(0,0,0))
        >
'''
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
# External Input parameters
key='stim'
fmin=10 # Hz
fmax = sf / 10 # Hz
sensitivity_function = lambda d : (fmax + fmin) - d * fmax / dmax

network[key] = pd.Series({'fmin':fmin, 'fmax':fmax, 'sensitivity_function':lambda v:v}) #sensitivity function is linear 

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
'''
Population and network default parameters
keys:
    >'population'
        >num
        >width
        >depth
'''
population = {}
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
key = 'default'
# Default Population parameters
num = 100
width = 1
height = 1
depth = 0

population[key] = pd.Series({'num':num,'width':width,'height':height, 'depth':depth})
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
key = 'trim'
# Default Population states
trim = False

population[key] = trim
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###


network_parameters= pd.DataFrame({
    'network':network,
    'population':population,
})

neuron_parameters = pd.DataFrame({
    'density_matrix':density_matrix,
    'delay_matrix':delay_matrix,
    'neuron_radius':neuron_radius,
    'color':color,
    'connectivity_distance':connectivity_distance,
    'connectivity_cell_type':connectivity_cell_type,
    'a':a,
    'b':b,
    'c':c,
    'd':d,
    'v':v,
    'u':u,
    'i':I
})

synapse_parameters = pd.DataFrame({'rs':rs, 'fs':fs, 'lts':lts,'ib':ib})

all_parameters = pd.concat([network_parameters, neuron_parameters, synapse_parameters])
