from __future__ import division
from time import time
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.misc as spms
from scipy import ndimage
import os

divisionFactor = 255
maxIntensity = 1.0 if divisionFactor==255 else 255.0

def writePixelValuesToFile(fp, id, data):
	row, col = data.shape
	for i in xrange(0, row):
		for j in xrange(0, col):
			fp.write( "_".join([ str(id), str(i+1), str(j+1) ]) + "," + str(data[i][j] * divisionFactor) + "\n")

def plotImage(imageData, title):
	plt.figure()
	plt.title(title)
	plt.imshow(imageData, cmap=plt.cm.gray, interpolation='nearest')
	plt.xticks(())
	plt.yticks(())

def intensify(cleaned, phi=1, theta=1, multiplier=2):
	cleaned = (maxIntensity/phi)*(cleaned/(maxIntensity/theta))**multiplier
	return cleaned
	
def applyFilter(input, filter, title, multiplier, intensifyFilter=True, showImage=True):
	#if showImage: plotImage(filter, title)
	if intensifyFilter: filter = intensify(filter, phi=1, theta=1, multiplier=multiplier)
	
	mask = input < filter - 0.1
	#if showImage: plotImage(mask, "mask : " + title)

	#cleaned = (input - filter)
	cleaned = np.where(mask, input, 1.0)
	#if showImage: plotImage(filter, title)
	#if showImage: plotImage(cleaned, "cleaned = input - " + title)
	
	#print title, " -> output-cleaned norm : ", np.linalg.norm(output-cleaned)
	return cleaned

testDir = "./test/"
fp = open("anil_submission.csv", "w")
fp.write("id,value\n")

for file in os.listdir("./test/"):
	id = os.path.splitext(file)[0]
	#print testDir + file
	print id

	x = testDir + file
	
	#x = "2.png"
	
	input = spms.imread(x)
	input = input / divisionFactor
	#plotImage(input, "input: distorted image")
	#plotImage(output, "output : cleaned image")
	maxFilterCleaned = applyFilter(input, ndimage.maximum_filter(input, size=3, origin=0), "maxFilter1", 1, False, True)
	writePixelValuesToFile(fp, id, maxFilterCleaned)
	#break

#plt.show()
fp.close()