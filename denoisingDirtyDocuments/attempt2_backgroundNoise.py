from __future__ import division
from time import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.misc as spms
from scipy import ndimage

divisionFactor = 255
maxIntensity = 1.0 if divisionFactor==255 else 255.0

def plotImage(imageData, title):
	plt.figure()
	plt.title(title)
	plt.imshow(imageData, cmap=plt.cm.gray, interpolation='nearest')
	plt.xticks(())
	plt.yticks(())

def intensify(cleaned, phi=1, theta=1):
	cleaned = (maxIntensity/phi)*(cleaned/(maxIntensity/theta))**2
	return cleaned
	
def applyFilter(input, filter, title):
	cleaned = input - filter
	plotImage(filter, title)
	plotImage(cleaned, "cleaned = input - " + title)
	return cleaned
	
x = "2.png"
y = "2_output.png"

input = spms.imread(x)
output = spms.imread(y)

#input, output = 1.0*input, 1.0*output

input = input / divisionFactor
output = output / divisionFactor
height, width = input.shape

plotImage(input, "input: distorted image")
plotImage(output, "output : cleaned image")
#maxFilterCleaned = applyFilter(input, ndimage.maximum_filter(input, size=5, mode='nearest'), "maxFilter")
#cleaned = applyFilter(input, ndimage.percentile_filter(input, percentile=98, size=5), "percentile_filter")
cleaned = applyFilter(input, ndimage.rank_filter(input, rank=-1, size=3), "percentile_filter")
#cleaned = applyFilter(cleaned, ndimage.gaussian_filter(cleaned, 2), "gaussian_filter")

plt.show()
