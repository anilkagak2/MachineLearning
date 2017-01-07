import numpy as np
from scipy.ndimage import imread 
from scipy import ndimage
from matplotlib import pyplot as plt
import sys
import os
import sklearn 
from sklearn.datasets import fetch_mldata
from sklearn import metrics, svm, cross_validation, datasets
from scipy.misc import imresize

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


mnist = fetch_mldata('MNIST original')

X = mnist.data
y = mnist.target
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=5000, train_size=10000)

#digits = datasets.load_digits()
#X = digits.images.reshape((len(digits.images), -1))
#y = digits.target
#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y)

print(len(y))

images = [ image.reshape((28,28)) for image in X ]

'''
#images_and_labels = list(zip(digits.images, digits.target))
images_and_labels = list(zip(images, y))
for index, (image, label) in enumerate(images_and_labels):
	if label == 7:
		print(image)
		plt.imshow(image, cmap='gray')
		plt.show()
		
		x = imresize(image, (8,8))
		plt.imshow(x, cmap='gray')
		plt.show()
		
		break
'''

print("test image")
lines = sys.stdin.read().strip().split("\n")

vals = [ line.split(" ") for line in lines[1:] ]
imgPixels = []
for y in vals:
    y = [ [ int(p) for p in u.split(",") ] for u in y ]
    imgPixels.append(y)

x = np.array(imgPixels)
plt.imshow(x)
plt.show()

#x = ndimage.gaussian_filter(x, sigma=3)

# reshape the input image to 28 x 28 
#x = imresize(x, (28,28))
print(x)
x = rgb2gray(x)

#x = x[:,:,0]
print(x)
plt.imshow(x, cmap='gray')
plt.show()
x = imresize(x, (8,8))
plt.imshow(x, cmap='gray')
plt.show()
#x = x[:,:,0]
x = x.flatten()
