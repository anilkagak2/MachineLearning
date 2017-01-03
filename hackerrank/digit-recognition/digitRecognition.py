import numpy as np
from scipy.ndimage import imread 
from matplotlib import pyplot as plt
import sys
import os
import pickle
import sklearn 
from sklearn.datasets import fetch_mldata
from sklearn import metrics, svm, cross_validation
from scipy.misc import imresize

mnist = fetch_mldata('MNIST original')

X = mnist.data
y = mnist.target
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=5000, train_size=5000)

print("training")
classifier = svm.SVC(gamma=0.001)
classifier.fit(X_train, y_train)

U = pickle.dumps(classifier)
print(len(U))

print("saving the baseencoded model")
import base64
Ubase64 = base64.b64encode(U)
with open("modelbase64.txt", "wb") as fp:
    fp.write(Ubase64)

with open("model.txt", "wb") as fp:
    fp.write(U)

print("Loading the model and then predicting on test set")
classifier = pickle.loads(U)
predicted = classifier.predict(X_test)
print(metrics.classification_report(y_test, predicted))
print(metrics.classification_report(y_test, predicted))

print("test image")
lines = sys.stdin.read().strip().split("\n")

vals = [ line.split(" ") for line in lines[1:] ]
imgPixels = []
for y in vals:
    y = [ [ int(p) for p in u.split(",") ] for u in y ]
    imgPixels.append(y)

x = np.array(imgPixels)

# reshape the input image to 28 x 28 
x = imresize(x, (28,28))
print(classifier.predict(x))