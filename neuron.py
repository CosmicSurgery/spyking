'''
NEURON ATTRIBUTES
    a
    b
    c
    d
    h
    I
    t
    u
    v
    x
    y
    cell_type
    fire
    group
    iMem
    input_synapses
    output_synapses
    position
    size
    spikes
    vMem
    uMem
NEURON PUBLIC METHODS
NEURON HIDDEN METHODS
'''

from parameters import neuron_parameters, all_parameters

cell_types=tuple(neuron_parameters.index)
neuron_radius = neuron_parameters.neuron_radius
izhikevich_parameters = neuron_parameters

class Neuron:

    def __init__(self, cell_type, group, x=None, y=None,z=None):
        self.cell_type = cell_type
        self.group = group

        self.assignPosition(x, y, z)
        self.input_synapses = []
        self.output_synapses = []
        self.resetParameters()
        self.setState()

    def tune(self,x,y):
        self.tunePOS = np.array(x,y)

    def setState(self):
        self.fire = False
        self.projection_neuron = False # True if this neuron projects to another population of neurons

    def resetParameters(self):
        self.size = neuron_parameters.neuron_radius[self.cell_type]
        self.a, self.b, self.c, self.d, self.v, self.u, self.I = tuple(neuron_parameters[['a','b','c','d','v','u','i']].loc[self.cell_type].values)
        self.color = neuron_parameters.color[self.cell_type]
        self.fr = 0
        self.t = 0
        self.vMem = []
        self.uMem = []
        self.iMem = []
        (_,_,self.h,self.sf) = all_parameters.network.timing
        self.spikes = []

    def assignPosition(self,x, y, z):
        self.x=x                                                                         # assignPosition assigns the neuron x and y
        self.y=y
        self.z=z
        self.position = (x, y, z)

    def attune(self,x,y,z):
        self.attunedPosition = np.array(x,y,z)

    def addInputSynapse(self, s):
        self.input_synapses += s

    def addOutputSynapse(self, s):
        self.output_synapses += s

    def sumI(self):
        return sum(self.I)
    
    def clearI(self):
        self.I = [0]

    def step(self):

        self.vMem.append(self.v)
        self.uMem.append(self.u)
        self.iMem.append(self.sumI())

        self.__Izhikevich()
        self.clearI()
        self.t = round(self.t + self.h, 1)

    def __Izhikevich(self):
        self.u, self.v = self.__discreteModel(self.a, self.b, self.u, self.v, self.sumI(), self.h)
        if self.v > 30:
            self.v = self.c
            self.u = self.u + self.d
            self.fire = True
            self.spikes.append(self.t)
        else:
            self.fire = False

    def __discreteModel(self, a, b, u, v, I, h):
        v= v + h *(0.04*v*v+5*v+140-u+I)                                                   
        u = u + h *(a*(b*v-u))
        return u,v

        

    def getFiringRate(self):
        self.fr = self.sf * self.h * len(self.spikes) / self.t # firing rate in Hz
        return self.fr

    def getMembraneConductance(self):
        pass