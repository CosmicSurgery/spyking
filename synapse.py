'''
SYNAPSE ATTRIBUTES
    conduction_delay
    input_neuron
    length
    output_neuron
    sf
    synapse_type
    weight

SYNAPSE METHODS
    step


diff EQ's:
    Vs(t) = Ts * Vs (t-1)
    Vf(t) = Tf * Vf (t-1)

'''

from parameters import all_parameters, neuron_parameters, synapse_parameters
import numpy as np
import random

class Synapse:

    def __init__ (self, input_neuron, output_neuron):
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron
        self.group = self.input_neuron.group
        
        self.T1,self.T2,self.h,self.sf = all_parameters.network.timing
        self.resetParameters()
        self.__setScaleFactor()
        self.__addSelf2Neurons()
        

    def resetParameters(self):
        self.setDelay(neuron_parameters['delay_matrix'][self.input_neuron.cell_type])
        self.__getLength(self.input_neuron, self.output_neuron)
        self.Vd = [0] * int(self.conduction_delay * self.sf )
        self.Vs = [0]
        self.Vf = [0]
        self.Vi = []
        self.Ts, self.Tf, self.Rs, self.Rf = tuple(synapse_parameters[self.input_neuron.cell_type][self.output_neuron.cell_type].values)
        self.v = 0
        self.f = all_parameters.network.stim.fmin
        self.t = 0
        self.spikes = []
        self.weight = 0
        self.stimF = []
        self.t_stim = None


    def __getLength(self, inp, out):
        if None not in inp.position  and None not in out.position:
            self.length = np.linalg.norm(np.array(inp.position)-np.array(out.position))

    def __addSelf2Neurons(self):
        if not self in self.input_neuron.output_synapses:
            self.input_neuron.output_synapses.append(self)
        if not self in self.output_neuron.input_synapses:
            self.output_neuron.input_synapses.append(self)

    def setDelay(self, delay):
        self.conduction_delay = delay

    def step(self):
        
        self.Vs.append(self.Vs[-1] * self.Ts)
        self.Vf.append(self.Vf[-1] * self.Tf)

        if self.input_neuron.fire:
            self.Vs[-1] += self.Rs
            self.Vf[-1] += self.Rf
            self.spikes.append(self.t)

        self.Vd.append((self.Vs[-1] - self.Vf[-1]) * self.scaling_factor + self.noise())
        self.Vi.append(self.Vd[0])
        self.sendCurrent()
        del(self.Vd[0])
        self.t = round(self.t + self.h, 1)
        
    def stim(self, f):
        if self.t_stim is None:
            if not self.stimF:
                self.stimF = [(self.h * self.sf)/k for k in list(np.random.poisson(f, 100))]
            temp_index = np.random.randint(0,len(self.stimF))
            self.t_stim = self.t + self.stimF[temp_index]
            del(self.stimF[temp_index])
        if self.t > self.t_stim:
            self.input_neuron.fire = True
            self.t_stim = None
        else:
            self.input_neuron.fire = False
        self.step()

    def sendCurrent(self):
        self.output_neuron.I.append(self.Vi[-1])

    def noise(self):
        return 0

    def variance(self, s):
        return 0

    def __setScaleFactor(self):
        self.scaling_factor = np.floor((-np.log(np.log(self.Tf)/np.log(self.Ts)))/(np.log(self.Tf)-np.log(self.Ts)))
        self.scaling_factor = (self.Ts**self.scaling_factor - self.Tf**self.scaling_factor)**(-1)

    def getFiringRate(self):
        if self.t != 0:
            self.fr = self.sf * self.h * len(self.spikes) / self.t # firing rate in Hz
            return self.fr
