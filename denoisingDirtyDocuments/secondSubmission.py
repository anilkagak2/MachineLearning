from __future__ import division
from scipy import signal
from PIL import Image
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
	
def denoise_image(inp):
    # estimate 'background' color by a median filter
    bg = signal.medfilt2d(inp, 11)
    #plotImage(bg, 'background.png')

    # compute 'foreground' mask as anything that is significantly darker than
    # the background
    mask = inp < bg - 0.1
    #plotImage(mask, 'foreground_mask.png')

    # return the input value for all pixels in the mask or pure white otherwise
    return np.where(mask, inp, 1.0)

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
	signalCleaned = denoise_image(input)
	signalCleaned = signalCleaned*255.0
	#plotImage(signalCleaned, " signal cleaned")
	writePixelValuesToFile(fp, id, signalCleaned)
	#break

plt.show()
fp.close()