# author: Piotr Andrzejewski

import numpy as np


def sigmoid(x):
    return 1.0/(1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


def relu(x):
    return x * (x > 0)


def relu_derivative(x):
    return 1. * (x > 0)


class NeuralNetwork(object):
    def __init__(self, x, y, activation_func, activation_derivative, eta):
        self.input = x
        self.weights1 = np.random.rand(4, self.input.shape[1])
        self.weights2 = np.random.rand(1, 4)
        self.y = y
        self.output = np.zeros(self.y.shape)
        self.eta = eta
        self.activation_func = activation_func
        self.activation_derivative = activation_derivative

    def feedforward(self):
        self.layer1 = self.activation_func(np.dot(self.input, self.weights1.T))
        self.output = self.activation_func(np.dot(self.layer1, self.weights2.T))

    def backprop(self):
        delta2 = (self.y - self.output) * self.activation_derivative(self.output)
        d_weights2 = self.eta * np.dot(delta2.T, self.layer1)
        delta1 = self.activation_derivative(self.layer1) * np.dot(delta2, self.weights2)
        d_weights1 = self.eta * np.dot(delta1.T, self.input)

        self.weights1 += d_weights1
        self.weights2 += d_weights2


def get_xor_input():
    X = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]])
    y = np.array([[0], [1], [1], [0]])
    return X, y


def get_and_input():
    X = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]])
    y = np.array([[0], [0], [0], [1]])
    return X, y


def get_or_input():
    X = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]])
    y = np.array([[1], [1], [1], [1]])
    return X, y


def get_network(X, y, is_sigmoid, eta):
    if is_sigmoid:
        activation_func = sigmoid
        activation_derivative = sigmoid_derivative
    else:
        activation_func = relu
        activation_derivative = relu_derivative
    return NeuralNetwork(X, y, activation_func, activation_derivative, eta)


def network_test(network):
    for i in range(5000):
        network.feedforward()
        network.backprop()
    return network.output


def make_test(X, y, is_sigmoid, seed, eta):
    np.random.seed(seed)
    network = get_network(X, y, is_sigmoid, eta)
    return network_test(network)


if __name__ == '__main__':
    # glowne pytanie: testujemy siec tylko na danych treningowych, czy rowniez na nowych?
    print("XOR, sigmoid\n", make_test(*get_xor_input(), is_sigmoid=True, seed=17, eta=0.5))
    print("XOR, ReLU\n", make_test(*get_xor_input(), is_sigmoid=False, seed=54, eta=0.01))
    print("AND, sigmoid\n", make_test(*get_and_input(), is_sigmoid=True, seed=1, eta=0.1))
    print("AND, ReLU\n", make_test(*get_and_input(), is_sigmoid=False, seed=17, eta=0.001))
    print("OR, sigmoid\n", make_test(*get_or_input(), is_sigmoid=True, seed=17, eta=0.5))
    print("OR, ReLU\n", make_test(*get_or_input(), is_sigmoid=False, seed=17, eta=0.1))

# Odpowiedź na pytanie:
#   ta ostatnia kolumna reprezentuje tzw. "bias", o którym była mowa w 3Blue1Brown,
#   który pozwala "przesunąć" próg, po przekroczeniu którego neuron staje się aktywny
