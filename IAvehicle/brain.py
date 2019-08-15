from IAvehicle.neuron import *
from copy import deepcopy
import numpy as np


class Network:
    """
        Class used to model a Neuronal Network
    """

    def __init__(self, pattern, nb_inputs=1):
        """
        :param pattern: {list} : pattern of the network
        :param nb_inputs: {int} : number of inputs for the first layer
        """

        self.__layers = []
        self.__pattern = pattern
        self.__genotype = []
        self.__nb_inputs = nb_inputs
        self.__output = 0

        for p in pattern:
            temp_layer = []
            for i in range(p):
                n = Neuron(nb_inputs)
                temp_layer.append(n)
                self.__genotype.append(n)

            self.__layers.append(deepcopy(temp_layer))
            nb_inputs = len(self.__layers[-1])

        self.performance = 0

    def update_pattern(self):
        """
            Update network's pattern based on current layers.
            Useful when layers is altered during evolution.
        :return:
        """
        temp_pattern = []
        for layer in self.__layers:
            temp_pattern.append(len(layer))

        self._set_pattern(temp_pattern)

    def __repr__(self):
        neuron = ""
        for layer in self.__layers:
            for n in layer:
                neuron += str(n) + " "
            neuron += "\n"

        return "--------------------\n" + str(self.__pattern) + "\n" + neuron + "--------------------\n"

    def get_layer_output(self, layer_index):
        """
            Method used to return outputs of one specified layer.
        :param layer_index: {int} : index of the layer
        :return:
        """

        outputs = []
        for n in self.layers[layer_index]:
            outputs.append(n.output)

        return outputs

    def feed_forward(self, inputs):
        """
            Propagate the data in the neuronal network.
        :param inputs: {List} : List of inputs for the first layer.
        :return:
        """
        if type(inputs) != list:
            raise TypeError("Inputs must be a list")
        elif len(inputs) != len(self.__layers[0][0].weights):
            raise IndexError("Input's number must be the same size as neuron's inputs")

        features = deepcopy(inputs)
        index = 0
        for layer in self.__layers:
            for n in layer:
                n.feed_forward(features)

            features = deepcopy(self.get_layer_output(index))
            index += 1

        self.__output = [d.output for d in self.__layers[-1]]

    def mutation(self):
        """
            Change randomly the weights and the bias of each neuron with the normal law.
        :return:
        """
        for layer in self.__layers:
            for n in layer:
                n.mutation()

    # Accessors and mutator
    def _get_pattern(self):
        return self.__pattern

    def _set_pattern(self, p):
        self.__pattern = p

    def _get_layers(self):
        return self.__layers

    def _set_layers(self, l):
        self.__layers = l

    def _get_genotype(self):
        return self.__genotype

    def _set_genotype(self, gen):
        self.__genotype = gen

    def _get_nb_inputs(self):
        return self.__nb_inputs

    def _set_nb_inputs(self, n):
        self.__nb_inputs = n

    pattern = property(_get_pattern, _set_pattern)
    layers = property(_get_layers, _set_layers)
    genotype = property(_get_genotype, _set_genotype)
    nb_inputs = property(_get_nb_inputs, _set_nb_inputs)
