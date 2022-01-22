import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        # TODO (Implement FCNNs architecture here)
        self.input_size = layer_sizes[0]
        self.hidden_size = layer_sizes[1]
        self.output_size = layer_sizes[2]
        self.w1 = np.random.standard_normal(size=(self.hidden_size, self.input_size))
        self.w2 = np.random.standard_normal(size=(self.output_size, self.hidden_size))
        self.b1 = np.zeros((self.hidden_size, 1))
        self.b2 = np.zeros((self.output_size, 1))
        


    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        # TODO (Implement activation function here)
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        x = x.reshape((self.input_size,1))
        # TODO (Implement forward function here)

        a1 = self.activation(self.w1 @ x + self.b1)


        a2 = self.activation(self.w2 @ a1 + self.b2)




        return a2
