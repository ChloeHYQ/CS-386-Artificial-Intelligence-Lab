# dataClassifier.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# This file contains feature extraction methods and harness
# code for data classification

import perceptron
import samples
import sys
import util

sys.setrecursionlimit(3000)

TEST_SET_SIZE = 1000
DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28
FACE_DATUM_WIDTH=60
FACE_DATUM_HEIGHT=70


def basicFeatureExtractorDigit(datum):
	"""
	Returns a set of pixel features indicating whether
	each pixel in the provided datum is white (0) or gray/black (1)
	"""
	a = datum.getPixels()

	features = util.Counter()
	for x in range(DIGIT_DATUM_WIDTH):
		for y in range(DIGIT_DATUM_HEIGHT):
			if datum.getPixel(x, y) > 0:
				features[(x,y)] = 1
			else:
				features[(x,y)] = 0
	return features

def enhancedFeatureExtractorDigit(datum):
	"""
	Your feature extraction playground.

	You should return a util.Counter() of features
	for this datum (datum is of type samples.Datum).

	## DESCRIBE YOUR ENHANCED FEATURES HERE...
	The enhanced features used are:
	1. The sum of pixel values in every row is added up and then we normalize these numbers. 
	   Then we add a bias(1 seemed to give the best results for my case). 
	2. The sum of pixel values in every column is added up and then we normalize these numbers. 
	   Then we add a bias(1 seemed to give the best results for my case). 
	3. Marking the outermost black region of the digit. This is done by marking the connected
	   component surrounding the digit. This is done by a dfs traversal starting from 0,0.
	   Here I have made an assumption that (0,0) pixel will necessarily be black in every case.
	   In this manner, we construct the visited matrix corresponding to the pixel values
	   Every pixel gets another feature for itself which is 0, if it belongs 
	   to the outermost black region surrounding the digit, that is the pixel was visited. 
	   Otherwise its value is 1.
	4. Vertical gradient - Every pixel gets another feature for itself which 
	   is defined as the absolute difference in the pixel values of the current pixel and 
	   the pixel just above it.
	
	Intuition behind the features:
	1 and 2 - It gives us the fraction of light pixels in every row or column as the case may be, 
			these features should be similar for similar number shapes
	3 - This sort of gives us an outer shape of the digit, and hence helps
	4 - These give us the edges of the digits obtained from vertical gradient. 
		The edge information also helps.
	##
	"""
	features =  basicFeatureExtractorDigit(datum)

	"*** YOUR CODE HERE ***"
	a = datum.getPixels()

	row_sum = []
	col_sum = []

	# Extracting row sum
	for x in range(DIGIT_DATUM_WIDTH):
		temp_row = 0
		row_sum.append(sum(a[x]))
	row_sum_tot = sum(row_sum)
	
	for i in range(DIGIT_DATUM_WIDTH):
		features[("row",i)] = 1.0 + row_sum[i]/row_sum_tot
		
	# Extracting column sum

	for y in range(DIGIT_DATUM_HEIGHT):
		temp_col = 0
		for x in range(DIGIT_DATUM_WIDTH):
			pix = datum.getPixel(x,y)
			temp_col += pix
		col_sum.append(temp_col)
	col_sum_tot = sum(col_sum)

	for i in range(DIGIT_DATUM_HEIGHT):
		features[("col",i)] = 1.0 + col_sum[i]/col_sum_tot

	visited = []

	for x in range(DIGIT_DATUM_WIDTH):
		temp = [0 for y in range(DIGIT_DATUM_HEIGHT)]
		visited.append(temp)

	def getNeighbors(x,y):
		nbrs = []
		if (x+1) < DIGIT_DATUM_WIDTH:
			nbrs.append((x+1,y))
		if (x-1) >= 0:
			nbrs.append((x-1,y))
		if (y+1) < DIGIT_DATUM_HEIGHT:
			nbrs.append((x,y+1))
		if (y-1) >= 0:
			nbrs.append((x,y-1))
		return nbrs



	def dfs_mark(x,y):
		if visited[x][y] == 1:
			return
		if datum.getPixel(x,y) == 0:
			visited[x][y] = 1
		else:
			return
		nbrs = getNeighbors(x,y)
		for nbr in nbrs:
			dfs_mark(nbr[0],nbr[1])

	dfs_mark(0,0)

	for x in range(DIGIT_DATUM_WIDTH):
		for y in range(DIGIT_DATUM_HEIGHT):
			# Features according to the visited map 
			# which gives us the outer shape of the digit
			if visited[x][y] == 1:
				features[((x,y),1)] = 0
			else:
				features[((x,y),1)] = 1

			# Vertical gradient calculation for the edges
			temp = datum.getPixel(x,y)
			temp_down = temp+0
			if y-1 >= 0:
				temp_down = datum.getPixel(x,y-1)
			temp = abs(temp-temp_down)
			features[((x,y),2)] = temp
	
	return features

def analysis(classifier, guesses, testLabels, testData, rawTestData, printImage):
	"""
	This function is called after learning.
	Include any code that you want here to help you analyze your results.

	Use the printImage(<list of pixels>) function to visualize features.

	An example of use has been given to you.

	- classifier is the trained classifier
	- guesses is the list of labels predicted by your classifier on the test set
	- testLabels is the list of true labels
	- testData is the list of training datapoints (as util.Counter of features)
	- rawTestData is the list of training datapoints (as samples.Datum)
	- printImage is a method to visualize the features
	(see its use in the odds ratio part in runClassifier method)

	This code won't be evaluated. It is for your own optional use
	(and you can modify the signature if you want).
	"""

	# Put any code here...
	# Example of use:
	# for i in range(len(guesses)):
	#     prediction = guesses[i]
	#     truth = testLabels[i]
	#     if (prediction != truth):
	#         print "==================================="
	#         print "Mistake on example %d" % i
	#         print "Predicted %d; truth is %d" % (prediction, truth)
	#         print "Image: "
	#         print rawTestData[i]
	#         break


## =====================
## You don't have to modify any code below.
## =====================


class ImagePrinter:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def printImage(self, pixels):
		"""
		Prints a Datum object that contains all pixels in the
		provided list of pixels.  This will serve as a helper function
		to the analysis function you write.

		Pixels should take the form
		[(2,2), (2, 3), ...]
		where each tuple represents a pixel.
		"""
		image = samples.Datum(None,self.width,self.height)
		for pix in pixels:
			try:
			# This is so that new features that you could define which
			# which are not of the form of (x,y) will not break
			# this image printer...
				x,y = pix
				image.pixels[x][y] = 2
			except:
				print "new features:", pix
				continue
		print image

def default(str):
	return str + ' [Default: %default]'

USAGE_STRING = """
  USAGE:      python dataClassifier.py <options>
  EXAMPLES:   (1) python dataClassifier.py
				  - trains the default mostFrequent classifier on the digit dataset
				  using the default 100 training examples and
				  then test the classifier on test data
			  (2) python dataClassifier.py -c perceptron -t 1000 -f -s 1000
				  - would run the perceptron classifier on 1000 training examples
				  using the enhancedFeatureExtractorDigits function to get the features
				  on the digits dataset, would test the classifier on the test data of 1000 examples
				 """


def readCommand( argv ):
	"Processes the command used to run from the command line."
	from optparse import OptionParser
	parser = OptionParser(USAGE_STRING)

	parser.add_option('-c', '--classifier', help=default('The type of classifier'), choices=['perceptron'], default='perceptron')
	parser.add_option('-t', '--training', help=default('The size of the training set'), default=1000, type="int")
	parser.add_option('-f', '--features', help=default('Whether to use enhanced features'), default=False, action="store_true")
	parser.add_option('-k', '--smoothing', help=default("Smoothing parameter (ignored when using --autotune)"), type="float", default=2.0)
	parser.add_option('-a', '--autotune', help=default("Whether to automatically tune hyperparameters"), default=False, action="store_true")
	parser.add_option('-i', '--iterations', help=default("Maximum iterations to run training"), default=3, type="int")
	parser.add_option('-s', '--test', help=default("Amount of test data to use"), default=TEST_SET_SIZE, type="int")
	parser.add_option('-v', '--validate', help=default("Whether to validate when training (for graphs)"), default=False, action="store_true")

	options, otherjunk = parser.parse_args(argv)
	if len(otherjunk) != 0: raise Exception('Command line input not understood: ' + str(otherjunk))
	args = {}

	# Set up variables according to the command line input.
	print "Doing classification"
	print "--------------------"
	print "classifier:\t\t" + options.classifier
	print "using enhanced features?:\t" + str(options.features)
	print "training set size:\t" + str(options.training)

	printImage = ImagePrinter(DIGIT_DATUM_WIDTH, DIGIT_DATUM_HEIGHT).printImage
	if (options.features):
		featureFunction = enhancedFeatureExtractorDigit
	else:
		featureFunction = basicFeatureExtractorDigit
	
	legalLabels = range(10)

	if options.training <= 0:
		print "Training set size should be a positive integer (you provided: %d)" % options.training
		print USAGE_STRING
		sys.exit(2)

	if options.smoothing <= 0:
		print "Please provide a positive number for smoothing (you provided: %f)" % options.smoothing
		print USAGE_STRING
		sys.exit(2)

	if(options.classifier == "perceptron"):
	   classifier = perceptron.PerceptronClassifier(legalLabels,options.iterations)
	else:
		print "Unknown classifier:", options.classifier
		print USAGE_STRING
		sys.exit(2)


	args['classifier'] = classifier
	args['featureFunction'] = featureFunction
	args['printImage'] = printImage

	return args, options

# Main harness code



def runClassifier(args, options):
	featureFunction = args['featureFunction']
	classifier = args['classifier']
	printImage = args['printImage']
	
	# Load data
	numTraining = options.training
	numTest = options.test

	rawTrainingData = samples.loadDataFile("digitdata/trainingimages", numTraining,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
	trainingLabels = samples.loadLabelsFile("digitdata/traininglabels", numTraining)
	rawValidationData = samples.loadDataFile("digitdata/validationimages", numTest,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
	validationLabels = samples.loadLabelsFile("digitdata/validationlabels", numTest)
	rawTestData = samples.loadDataFile("digitdata/testimages", numTest,DIGIT_DATUM_WIDTH,DIGIT_DATUM_HEIGHT)
	testLabels = samples.loadLabelsFile("digitdata/testlabels", numTest)


	# Extract features
	print "Extracting features..."
	trainingData = map(featureFunction, rawTrainingData)
	validationData = map(featureFunction, rawValidationData)
	testData = map(featureFunction, rawTestData)

	# Conduct training and testing
	print "Training..."
	classifier.train(trainingData, trainingLabels, validationData, validationLabels, options.validate)
	print "Validating..."
	guesses = classifier.classify(validationData)
	correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
	print str(correct), ("correct out of " + str(len(validationLabels)) + " (%.1f%%).") % (100.0 * correct / len(validationLabels))
	
	if(options.classifier == "perceptron"):
		f = open("perceptron_valid.csv","a")
		f.write(str(len(trainingData))+","+str(100*correct/(1.0*(len(validationData))))+'\n')
		f.close()
	
	print "Testing..."
	guesses = classifier.classify(testData)
	correct = [guesses[i] == testLabels[i] for i in range(len(testLabels))].count(True)
	print str(correct), ("correct out of " + str(len(testLabels)) + " (%.1f%%).") % (100.0 * correct / len(testLabels))
	analysis(classifier, guesses, testLabels, testData, rawTestData, printImage)
	
	if(options.classifier == "perceptron"):
		f = open("perceptron_test.csv","a")
		f.write(str(len(trainingData))+","+str(100*correct/(1.0*(len(testData))))+'\n')
		f.close()
		

if __name__ == '__main__':
	# Read input
	args, options = readCommand( sys.argv[1:] )
	# Run classifier
	runClassifier(args, options)
