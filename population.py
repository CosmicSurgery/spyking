'''
POPULATION ATTRIBUTES
    net
    num
    height
    width

POPULATION METHODS
    __setup
        __generateNeurons
            __legalPlacement
                __randomNeuronType
                    __assign
        __generateSynapses
            __doesConnect
            __formConnections
        __trimCortex
        __random_fix
        __sync



'''


from parameters import neuron_parameters, all_parameters, np
from neuron import Neuron
from synapse import Synapse
import random

class Population:

    def __init__(self, net, group):
        self.net = net 
        self.group = group
        self.__setParameters()
        self.__setup()

    def __setState(self):
        self.trim = all_parameters.population.trim

    def __setParameters(self):
        self.num, self.width, self.height, self.depth = tuple(all_parameters.population.default.values)
        self.neurons = []
        self.synapses = []
        self.trim = all_parameters.population.trim

    def __setup(self):
        self.__populateNeurons()
        self.__populateSynapses()
        if self.trim:
            self.__trimCortex()
        else:
            self.__random_fix()
        self.__sync()
        self.net.groups.append(self)

    def __populateNeurons(self):
        for i in range(self.num):
            while not self.__legalPlacement(i, self.neurons):
                pass
    
    def __legalPlacement(self, i, neurons):
        x, y, z = random.uniform(self.net.width, self.net.width + self.width), random.uniform(0, self.height), self.net.depth
        for k in neurons:
            if np.linalg.norm(np.array(k.position) - np.array([x,y,z])) <= k.size:
                return False
        neurons.append(self.__assignNeuronType())
        neurons[i].assignPosition(x,y,z)
        neurons[i].group = self.group
        return True
         
    def __assignNeuronType(self):
        range_max = sum(neuron_parameters.density_matrix.values)
        for cell_type in neuron_parameters.index:
            if random.randrange(0, int(range_max)) < neuron_parameters.density_matrix[cell_type]:
                return Neuron(cell_type, self.group)
            range_max -= neuron_parameters.density_matrix[cell_type]

    def __populateSynapses(self):
        for i in range(self.num):
            for j in range(self.num):
                if i != j and self.__doesConnect(self.neurons[i],self.neurons[j]) :
                    self.__formConnections(self.neurons[i],self.neurons[j])

    '''
    __doesConnect takes in a pre-synaptic neuron and a post-synaptic neuron and determines if they will form a synapse
    according to certain connecting probability distributions outlined in SNNconnectivity
    '''
    
    def __doesConnect(self, pre, post):
        scale  = len(neuron_parameters.connectivity_distance[pre.cell_type])
        distance_index = int(np.round(scale * np.linalg.norm(np.array(pre.position)-np.array(post.position)))) 
        # If distance is out of range of the cellRange distribution it is set to the smallest probability in the distribution
        if distance_index >= scale:
            distance_index = scale-1
        connection_probability = (
            neuron_parameters.connectivity_distance[pre.cell_type][distance_index] * neuron_parameters.connectivity_cell_type[pre.cell_type][post.cell_type])

        if random.uniform(0,1) < connection_probability:       #randomly determines draws from the distribution
            return True
        else:
            return False

    # creates a synapse object and appends it to the synapse list
    def __formConnections(self,inp,out):
        self.synapses.append(Synapse(inp, out))

    # randomly connect neurons that are either without an input or an output (alternative to trimming the cortex)
    def __random_fix(self):
        alone_neurons = [k for k in self.neurons if (not k.output_synapses and not k.input_synapses)]
        for k in alone_neurons:
            new_neuron = k
            while new_neuron == k: #Need while loop to make sure new_neuron does not select itself
                new_neuron = self.neurons[random.randrange(0,len(self.neurons))] 
            if not k.output_synapses:
                self.__formConnections(k, new_neuron)
            elif not k.input_synapses:
                self.__formConnections(new_neuron, k)

    # remove all redundant synapses and neurons from the cortex
    def __trimCortex(self):
        changed = True
        while changed:
            changed = False
            for i,k in enumerate(self.neurons):
                if not(k.output_synapses and k.input_synapses):
                    del(self.neurons[i])
                    changed = True
            for i,k in enumerate(self.synapses):
                temp_condition = not(k.input_neuron.input_synapses and k.out.output_synapses)
                if temp_condition:
                    changed = True
                    k.input_neuron.output_synapses = [s for s in k.input_neuron.output_synapses if s == self]
                    k.output_neuron.input_synapses = [s for s in k.output_neuron.input_synapses if s == self]
                    del(self.synapses[i])       

    def __sync(self):
        if self.depth:
            self.net.depth += self.depth
        else:
            self.net.width += self.width *1.5
            self.net.neurons += self.neurons
            self.net.synapses += self.synapses
    