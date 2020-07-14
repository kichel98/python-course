import matplotlib.pyplot as plt

import numpy as np


class FunctionWithDerivative:
    def __init__(self, function, derivative):
        self.function = function
        self.derivative = derivative


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1.0 - x)


def relu(x):
    return x * (x > 0)


def relu_derivative(x):
    return 1. * (x > 0)


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return (1. / np.cosh(x)) ** 2


class NeuralNetwork(object):
    def __init__(self, x, y, activation_layer1, activation_layer2, activation_layer3, eta):
        self.input = x
        self.weights1 = np.random.rand(10, self.input.shape[1])
        self.weights2 = np.random.rand(10, 10)
        self.weights3 = np.random.rand(1, 10)
        self.y = y
        self.output = np.zeros(self.y.shape)
        self.eta = eta
        self.activation_layer1 = activation_layer1
        self.activation_layer2 = activation_layer2
        self.activation_layer3 = activation_layer3

    def feedforward(self):
        self.layer1 = self.activation_layer1.function(np.dot(self.input, self.weights1.T))
        self.layer2 = self.activation_layer2.function(np.dot(self.layer1, self.weights2.T))
        self.output = self.activation_layer3.function(np.dot(self.layer2, self.weights3.T))

    def backprop(self):
        delta3 = (self.y - self.output) * self.activation_layer3.derivative(self.output)
        d_weights3 = self.eta * np.dot(delta3.T, self.layer2)
        delta2 = self.activation_layer2.derivative(self.layer2) * np.dot(delta3, self.weights3)
        d_weights2 = self.eta * np.dot(delta2.T, self.layer1)
        delta1 = self.activation_layer3.derivative(self.layer1) * np.dot(delta2, self.weights2)
        d_weights1 = self.eta * np.dot(delta1.T, self.input)

        self.weights1 += d_weights1
        self.weights2 += d_weights2
        self.weights3 += d_weights3


def test_parabolic():
    x = np.linspace(-50, 50, 26).reshape((-1, 1))
    y = x**2
    plt.subplot(2, 1, 1)
    plt.scatter(x, y)
    network = NeuralNetwork(x, y, FunctionWithDerivative(sigmoid, sigmoid_derivative),
                            FunctionWithDerivative(tanh, tanh_derivative),
                            FunctionWithDerivative(sigmoid, sigmoid_derivative), 0.00001)
    for i in range(20000):
        network.feedforward()
        network.backprop()
    x2 = np.linspace(-50, 50, 101).reshape((-1, 1))
    network.input = x2
    network.feedforward()
    y2 = network.output
    plt.subplot(2, 1, 2)
    plt.scatter(x2, y2)
    plt.show()


def test_sinus():
    x = np.linspace(0, 2, 21).reshape((-1, 1))
    y = np.sin((3 * np.pi / 2) * x)
    plt.subplot(2, 1, 1)
    plt.scatter(x, y)
    network = NeuralNetwork(x, y, FunctionWithDerivative(tanh, tanh_derivative),
                            FunctionWithDerivative(tanh, tanh_derivative),
                            FunctionWithDerivative(tanh, tanh_derivative), 0.01)
    for i in range(20000):
        network.feedforward()
        network.backprop()
    x2 = np.linspace(0, 2, 161).reshape((-1, 1))
    network.input = x2
    network.feedforward()
    y2 = network.output
    plt.subplot(2, 1, 2)
    plt.scatter(x2, y2)
    plt.show()


if __name__ == '__main__':
    np.random.seed(17)
    test_parabolic()
    np.random.seed(17)
    test_sinus()
