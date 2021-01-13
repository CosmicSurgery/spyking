from synapse import Synapse
from neuron import Neuron
from parameters import all_parameters
from operator import attrgetter

import numpy as np

class Network:
    def __init__(self):
        self.cleanNetwork()
        self.setDefaults()
        self.taskAttributes()

    def cleanNetwork(self):
        self.neurons = []
        self.synapses = []
        self.groups = []

    def setDefaults(self):
        self.width=0
        self.height=0
        self.depth=0
        self.target_position=None
        self.cursor_position=None
        self.T1,self.T2,self.h,self.sf = all_parameters.network.timing

    def clearMemory(self):
        for s in self.synapses:
            s.resetParameters()
        for n in self.neurons:
            n.resetParameters()

    def taskAttributes(self):
        self.fmax, self.fmin = all_parameters.network.stim.fmax, all_parameters.network.stim.fmin
        self.dmax = np.sqrt(2)

    def formConnections(self, inp, out):
        self.synapses.append(Synapse(inp,out))
        
    def connectGroups(self,one, two, num_connections):
        output_neurons = self.getInputNeurons(one, num_connections)
        input_neurons = self.getInputNeurons(two, num_connections)
        for i in range(num_connections):
            input_neurons[i].group, output_neurons[i].group = 'projection', 'projection'
            input_neurons[i].color, output_neurons[i].color = 'pink', 'pink'
            self.formConnections(output_neurons[i] , input_neurons[i])

    def getNeuronsFromGroup(self,group):
        return [k for k in self.neurons if k.group == group]

    '''
    get OutputNeurons // getInputNeurons simply returns a list of neurons according to certain parameters
    cell_type - which cell types should be considered
    '''
    
    
    def getOutputNeurons(self, pop, num_connections, cell_filter = ['rs', 'ib']): # defaults to choose only excitatory neurons
        return [k for k in self.neurons if (attrgetter('cell_type')(k) in cell_filter and attrgetter('group')(k) == pop.group)]
    
    def getInputNeurons(self, pop, num_connections, cell_filter = ['rs', 'ib']): # defaults to choose only excitatory neurons
        return [k for k in self.neurons if (attrgetter('cell_type')(k) in cell_filter and attrgetter('group')(k) == pop.group)]

    def run(self):
        clk = np.arange(self.T1, self.T2, self.h)
        isTask = lambda s:(s.group=='task')
        for t in clk:
            for n in self.neurons:
                n.step()
            for s in self.synapses:
                if s.group=='task':
                    s.stim(self.sensitivity_function(s))
                elif s.group =='test':
                    s.stim(s.f)
                else:
                    s.step()
            
            if not int(t*10)%1000:
                completed = int(t*100) / (self.T2)
                print('%s %% completed' % completed)
            
        
    def sensitivity_function(self, s):
        d = np.linalg.norm(np.array(s.output_neuron.position)-np.array(self.target_position))
        return self.fmax * np.e**(-4*(d/self.dmax)**2)
        #return (self.fmax  + (d / self.dmax) *( self.fmin - self.fmax)) * np.e**(-6*(d / self.dmax )**2)

    def __computeStimFrequency(self, s):
        difference = np.linalg.norm(np.array(s.output_neuron.position)-np.array(self.target_position))
        coefficient = all_parameters.network.stim.sensitivity_function(difference)
        if not coefficient:
            coefficient = 0.0000001
        s.f = min(all_parameters.network.stim.fmax, all_parameters.network.stim.f / coefficient)
        
    def populateWith(self, objects):
        for k in objects:
            if type(k) == Neuron:
                self.neurons.append(k)
            elif type(k) == Synapse:
                self.synapses.append(k)

    def getNeuralResponse(self):
        self.neuralResponse = []
        for n in self.neurons:
            self.neuralResponse.append(n.getFiringRate())
        return self.neuralResponse

    def printNetworkComposition(self):
        for g in net.groups:
            print(g.group +'\n')
            for x in ['rs','fs','lts','ib']:
                print(str(len([k for k in net.neurons if k.cell_type == x and k.group == g.group])) + ' ' + x)



