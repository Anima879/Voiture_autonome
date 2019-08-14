from IAvehicle.neuron import *
from copy import deepcopy
import numpy as np


class Network:
    """
        Class used to model a Neuronal Network
    """

    def __init__(self, pattern, nb_inputs=1):
        """
        :param pattern:
        :param nb_inputs:
        """

        self.__layers = []
        self.__pattern = pattern
        self.__genotype = []
        self.__nb_inputs = nb_inputs
        self.__quad_error = 0
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

    def set_performance(self, perf):
        self.performance = perf

    def update_pattern(self):
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

    @staticmethod
    def mean(tab, value):
        return tab.count(value) / len(tab) * 100

    def _get_layer_output(self, layer_index):
        """
            Method used to return layer's outputs
        :param layer_index: {int} : index of the layer
        :return:
        """

        outputs = []
        for n in self.__layers[layer_index]:
            outputs.append(n._get_output())

        return outputs

    def feed_forward(self, inputs):
        """
        :param inputs: {List} : List of inputs for the first layer.
        :return:
        """
        if type(inputs) != list:
            raise TypeError("Inputs must be a list")
        elif len(inputs) != len(self.__layers[0][0]._get_weights()):
            raise IndexError("Input's number must be the same size as neuron's inputs")

        features = deepcopy(inputs)
        index = 0
        for layer in self.__layers:
            for n in layer:
                n.feed_forward(features)

            features = deepcopy(self._get_layer_output(index))
            index += 1

        self.__output = [d._get_output() for d in self.__layers[-1]]

    def mutation(self):
        for layer in self.__layers:
            for n in layer:
                n.mutation()

    def quad_error(self, target):
        """

        :param target:
        :return:
        """

        print("Output : ", self._get_layer_output(len(self.__layers) - 1))
        self.__quad_error = (target - self._get_layer_output(len(self.__layers) - 1)[0]) ** 2
        return self.__quad_error

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

    def _get_quad_error(self):
        return self.__quad_error


class DeepNetwork:
    """
        Model a neural network without using neuron object.
        Uses array instead.
        First item in pattern is the number of entry.
    """

    @property
    def layers(self):
        return self.__layers

    def __init__(self, pattern):
        self.__layers = []
        self.__results = []
        self.__performance = 0
        self.__nb_inputs = pattern[0]
        self.__delta = []
        self.__error = []

        temp_list = []
        for i in range(0, pattern[0]):
            temp_list.append([0])

        self.__inputs = np.array(temp_list)
        self.__layers.append(self.__inputs)

        self.__delta.append(0)
        for i in range(1, len(pattern)):
            self.__layers.append(np.random.normal(size=(pattern[i], len(self.__layers[i - 1]) + 1)))
            self.__delta.append(0)

        print(self.__delta)

    def feed_forward(self, inputs):
        """
            Propage le signal en avant avec les entrées données.
        :param inputs: {list} : Liste des entrées.
        :return: {list} : Liste des sorties de chaque couche sous forme {numpy.ndarray}
        """

        self.__results = []

        temp = []
        for elt in inputs:
            temp.append([elt])

        temp.append([1]) # Pour les bases de chaque neurone
        self.__results.append(np.array(temp))

        if len(inputs) != len(self.__inputs):
            raise ValueError("Nombre d'entrées invalides")

        for i in range(1, len(self.__layers)):
            self.__results.append(1 / (1 + np.exp(-np.dot(self.__layers[i], self.__results[i - 1]))))

        return self.__results


    # Getters and setters
    def _set_layers(self, l):
        self.__layers = l

    def _get_layers(self):
        return self.__layers

    def _set_performance(self, p):
        self.__performance = p

    def _get_performance(self):
        return self.__performance

    def _set_nb_inputs(self, n):
        self.__nb_inputs = n

    def _get_nb_inputs(self):
        return self.__nb_inputs

    def _set_inputs(self, i):
        self.__inputs = i

    def _get_inputs(self):
        return self.__inputs

    def _set_results(self, r):
        self.__results = r

    def _get_results(self):
        return self.__results

    def _set_delta(self, d):
        self.__delta = d

    def _get_delta(self):
        return self.__delta

    def _set_error(self, e):
        self.__error = e

    def _get_error(self):
        return self.__error

    results = property(_get_results, _set_results)
    inputs = property(_get_inputs, _set_inputs)
    layers = property(_get_layers, _set_layers)
    performance = property(_get_performance, _set_performance)
    nb_inputs = property(_get_nb_inputs, _set_nb_inputs)
    delta = property(_get_delta, _set_delta)
    error = property(_get_error, _set_error)


def main():
    pattern = [2, 3, 1]
    nn = DeepNetwork(pattern)

    for i in range(0, len(nn.layers)):
        print("Couche : ", i)
        print(nn.layers[i])
        print("-----------------------------------")
        print(np.split(nn.layers[i], [nn.layers[i].shape[1] - 1], axis=1)[0])

    print("----------Feed forward----------")
    liste = nn.feed_forward([1, 1])
    for elt in liste:
        print(elt)
    print(float(liste[-1]))

    print("----------Feed backward----------")
    nn.feed_backward(1)
    print(nn.delta)


if __name__ == "__main__": main()
