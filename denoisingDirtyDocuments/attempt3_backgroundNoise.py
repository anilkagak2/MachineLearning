from __future__ import division
from time import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.misc as spms
from scipy import ndimage

divisionFactor = 1.0
maxIntensity = 1.0 if divisionFactor==255 else 255.0

def writePixelValuesToFile(file, id, data):
	f = open(file,'w')
	row, col = data.shape
	for i in xrange(0, row):
		for j in xrange(0, col):
			f.write( "_".join([ str(id), str(i), str(j) ]) + "," + str(data[i][j]) + "\n")
	f.close()

def plotImage(imageData, title):
	plt.figure()
	plt.title(title)
	plt.imshow(imageData, cmap=plt.cm.gray, interpolation='nearest')
	plt.xticks(())
	plt.yticks(())

def intensify(cleaned, phi=1, theta=1, multiplier=2):
	cleaned = (maxIntensity/phi)*(cleaned/(maxIntensity/theta))**multiplier
	return cleaned
	
def applyFilter(output, input, filter, title, multiplier, intensifyFilter=True, showImage=True):
	if showImage: plotImage(filter, title)
	if intensifyFilter: filter = intensify(filter, phi=1, theta=1, multiplier=multiplier)
	cleaned = (input - filter) + 255.0
	if showImage: plotImage(filter, title)
	plotImage(cleaned, "cleaned = input - " + title)
	
	print title, " -> output-cleaned norm : ", np.linalg.norm(output-cleaned)
	return cleaned
	
x = "2.png"
y = "2_output.png"

input = spms.imread(x)
output = spms.imread(y)

#input, output = 1.0*input, 1.0*output

input = input / divisionFactor
output = output / divisionFactor
height, width = input.shape
print input.shape
plotImage(input, "input: distorted image")
plotImage(output, "output : cleaned image")
maxFilterCleaned = applyFilter(output, input, ndimage.maximum_filter(input, size=3, origin=1), "maxFilter1", 1, False, False)

writePixelValuesToFile("cleaned.csv", 2, maxFilterCleaned)
writePixelValuesToFile("output.csv", 2, output)

plt.show()
