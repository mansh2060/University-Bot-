# creating a neural network with  input layers , hidden layer 1 , hidden layer 2  and output layer


import torch
import torch.nn as nn

class NeuralNetwork(nn.Module):
    def __init__(self,input_layer,hidden_layer,output_layer):
        super(NeuralNetwork,self).__init__()            #initializing nn.module super class it contains all nn
        self.l1=nn.Linear(input_layer,hidden_layer)     # 1st connection between 1st layer and second layer
        self.l2=nn.Linear(hidden_layer,hidden_layer)    # 2nd connection between second layer and third layer
        self.l3=nn.Linear(hidden_layer,output_layer)    #3rd connection between third layer and output layer
        self.relu = nn.ReLU()

    def forward(self,inputs):
        output=self.l1(inputs)         #passing input to the 1st layer i.e  inputs=(input * weight + bias)
        output=self.relu(output)       #obtaining output after passing through activation function i.e  relu(inputs)  
        output=self.l2(output)         #providing output of 1st layer(input-hidden layer1) to the hidden layer 2
        output=self.relu(output)       #providing output to the activation function
        output=self.l3(output)         #getting output from last layer i.e from hidden-layer and output layer
        return output