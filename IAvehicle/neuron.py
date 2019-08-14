import math as m
from random import normalvariate, randint


class Neuron:
    """
        Class used to model a neuron
    """
    learn_rate = 0.8

    def __init__(self, nb_inputs):
        """
        :param nb_inputs: {int} Number of inputs.
        """
        self.__weights = []
        self.__bias = 0
        self.__output = 0

        for i in range(nb_inputs):
            self.__weights.append(normalvariate(0, 0.001))

    def __str__(self):
        return "Poids : " + str(self.__weights) + " Bias : " + str(self.__bias) + " Output : " + str(self.__output)

    @staticmethod
    def sigmoid(x):
        try:
            return 1 / (1 + m.exp(-x))
        except OverflowError:
            if x < 0:
                return 0
            else:
                return 1

    @staticmethod
    def tanh(x):
        return (m.exp(x) - m.exp(-x)) / (m.exp(x) + m.exp(-x))

    def feed_forward(self, inputs):
        result = 0
        for x, w in zip(inputs, self.__weights):
            result += x * w

        self.__output = self.sigmoid(result + self.__bias)
        # self.__output = self.tanh(result + self.__bias)

    def mutation(self):
        for i in range(len(self.__weights)):
            if randint(1, 4) == 1:
                self.__weights[i] += normalvariate(0, Neuron.learn_rate)

        if randint(1, 5) == 2:
            self.__bias += normalvariate(0, Neuron.learn_rate)

    def _set_output(self, out):
        self.__output = out

    def _get_output(self):
        return self.__output

    def _get_weights(self):
        return self.__weights

    def _set_weights(self, w):
        for i in range(len(self.__weights)):
            self.__weights[i] = w[i]

    output = property(_get_output, _set_output)
    weights = property(_get_weights, _set_weights)

    @classmethod
    def set__learn_rate(cls, learn_rate):
        Neuron.learn_rate = learn_rate


def main():
    n = Neuron(2)
    n.feed_forward([1, 1])
    print(n.output)

    n.mutation()
    n.feed_forward([1, 1])
    print(n.output)

    print(n)


if __name__ == "__main__": main()
