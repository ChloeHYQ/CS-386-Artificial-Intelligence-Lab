import nn
import numpy as np
import sys

from util import *
from visualize import *



# XTrain - List of training input Data
# YTrain - Corresponding list of training data labels
# XVal - List of validation input Data
# YVal - Corresponding list of validation data labels
# XTest - List of testing input Data
# YTest - Corresponding list of testing data labels


def taskLinear():
	XTrain, YTrain, XVal, YVal, XTest, YTest = readLinear()
	# Create a NeuralNetwork object 'nn1' as follows with optimal parameters. For parameter definition, refer to nn.py file.
	# nn1 = nn.NeuralNetwork(inputSize, outputSize, numHiddenLayers, hiddenLayerSizes, alpha, batchSize, epochs)
	
	###############################################
	# TASK 2.1 - YOUR CODE HERE

	nn1 = nn.NeuralNetwork(len(XTrain[0]), len(YTrain[0]), 0, [], 0.5, 1, 5)
	
	###############################################

	nn1.train(XTrain, YTrain, XVal, YVal, False, True)
	pred, acc = nn1.validate(XTest, YTest)
	print('Test Accuracy ',acc)
	# Run script visualizeTruth.py to visualize ground truth. Run command 'python3 visualizeTruth.py 1'
	# Use drawLinear(XTest, pred) to visualize YOUR predictions.
	drawLinear(XTest, pred)

def taskSquare():
	XTrain, YTrain, XVal, YVal, XTest, YTest = readSquare()
	# Create a NeuralNetwork object 'nn1' as follows with optimal parameters. For parameter definition, refer to nn.py file.
	# nn1 = nn.NeuralNetwork(inputSize, outputSize, numHiddenLayers, hiddenLayerSizes, alpha, batchSize, epochs)	
	
	###############################################
	# TASK 2.2 - YOUR CODE HERE
	nn1 = nn.NeuralNetwork(len(XTrain[0]), len(YTrain[0]), 1, [4], 0.1, 4, 10)

	
	###############################################
	
	nn1.train(XTrain, YTrain, XVal, YVal, False, True)
	pred, acc = nn1.validate(XTest, YTest)
	print('Test Accuracy ',acc)
	# Run script visualizeTruth.py to visualize ground truth. Run command 'python3 visualizeTruth.py 2'
	# Use drawSquare(XTest, pred) to visualize YOUR predictions.
	drawSquare(XTest, pred)


def taskCircle():
	XTrain, YTrain, XVal, YVal, XTest, YTest = readCircle()
	# Create a NeuralNetwork object 'nn1' as follows with optimal parameters. For parameter definition, refer to nn.py file.
	# nn1 = nn.NeuralNetwork(inputSize, outputSize, numHiddenLayers, hiddenLayerSizes, alpha, batchSize, epochs)
	
	###############################################
	# TASK 2.3 - YOUR CODE HERE
	nn1 = nn.NeuralNetwork(len(XTrain[0]), len(YTrain[0]), 1, [6], 0.1, 8, 10)
	
	###############################################

	nn1.train(XTrain, YTrain, XVal, YVal, False, True)
	pred, acc = nn1.validate(XTest, YTest)
	print('Test Accuracy ',acc)
	# Run script visualizeTruth.py to visualize ground truth. Run command 'python3 visualizeTruth.py 3'
	# Use drawCircle(XTest, pred) to visualize YOUR predictions.
	drawCircle(XTest, pred)


def taskSemiCircle():
	XTrain, YTrain, XVal, YVal, XTest, YTest = readSemiCircle()
	# Create a NeuralNetwork object 'nn1' as follows with optimal parameters. For parameter definition, refer to nn.py file.
	# nn1 = nn.NeuralNetwork(inputSize, outputSize, numHiddenLayers, hiddenLayerSizes, alpha, batchSize, epochs)
	
	###############################################
	# TASK 2.4 - YOUR CODE HERE
	
	nn1 = nn.NeuralNetwork(len(XTrain[0]), len(YTrain[0]), 1, [2], 0.2, 3, 10)
	
	###############################################

	nn1.train(XTrain, YTrain, XVal, YVal, False, True)
	pred, acc  = nn1.validate(XTest, YTest)
	print('Test Accuracy ',acc)
	# Run script visualizeTruth.py to visualize ground truth. Run command 'python3 visualizeTruth.py 4'
	# Use drawSemiCircle(XTest, pred) to visualize YOUR predictions.
	drawSemiCircle(XTest, pred)

def taskMnist():
	XTrain, YTrain, XVal, YVal, XTest, YTest = readMNIST()
	# Create a NeuralNetwork object 'nn1' as follows with optimal parameters. For parameter definition, refer to nn.py file.
	# nn1 = nn.NeuralNetwork(inputSize, outputSize, numHiddenLayers, hiddenLayerSizes, alpha, batchSize, epochs)
	
	###############################################
	# TASK 3 - YOUR CODE HERE
	# nn1 = nn.NeuralNetwork(len(XTrain[0]), len(YTrain[0]), 1, [16], 1, 8, 20)
	nn1 = nn.NeuralNetwork(len(XTrain[0]), len(YTrain[0]), 3, [50,50,50], 0.05, 16, 20)
	
	###############################################
	
	nn1.train(XTrain, YTrain, XVal, YVal, True, True)
	pred, acc = nn1.validate(XTest, YTest)
	print('Test Accuracy ',acc)
