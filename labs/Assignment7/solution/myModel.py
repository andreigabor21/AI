'''
A. In the file myModel.py, declare a class Net that suits your problem (the one from
example should work if you require just one hidden layer with linear activation).
'''

import torch
import torch.nn.functional as F


class Net(torch.nn.Module):
    # the class for the network

    def __init__(self, n_feature, n_hidden, n_output):
        # we have two layers: a hidden one and an output one
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.output = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x):
        # a function that implements the forward propagation of the signal
        # observe the relu function applied on the output of the hidden layer
        # x = F.tanh(self.hidden(x))
        x = torch.tanh(self.hidden(x))
        x = self.output(x)
        return x