import numpy as np
from scipy.ndimage import imread 
from scipy import ndimage
from matplotlib import pyplot as plt
import sys
import os
import pickle
import sklearn 
from sklearn.datasets import fetch_mldata
from sklearn import metrics, svm, cross_validation, datasets
from scipy.misc import imresize
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn import datasets, neighbors, linear_model

def brightenTestImage(x):
	plt.imshow(x, cmap='gray')
	plt.show()
	x = ndimage.filters.gaussian_filter(x, 3)
	plt.imshow(x, cmap='gray')
	plt.show()
	x = ndimage.label(x)[0]
	plt.imshow(x, cmap='gray')
	plt.show()
	#x *= 255.0/x.max()
	return x

def brightenImage(x):
	#plt.imshow(x, cmap='gray')
	#plt.show()
	#x = ndimage.filters.gaussian_filter(x, 3)
	#plt.imshow(x, cmap='gray')
	#plt.show()
	x = ndimage.label(x)[0]
	#plt.imshow(x, cmap='gray')
	#plt.show()
	#x *= 255.0/x.max()
	return x

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    gray *= 255.0/gray.max()
    return gray
	
newshape = (28,28)
	
mnist = fetch_mldata('MNIST original')
X = mnist.data
y = mnist.target
X = [ imresize(brightenImage(x.reshape((28,28))), newshape).flatten() for x in X ]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=5000, train_size=50000)

#digits = datasets.load_digits()
#X = digits.images.reshape((len(digits.images), -1))
#y = digits.target
#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y)

print(len(y))
'''
images = [ imresize(x.reshape((28,28)), newshape) for x in X ]
images_and_labels = list(zip(images, y))
for index, (image, label) in enumerate(images_and_labels):
	if label == 7:
		print(image)
		plt.imshow(image, cmap='gray')
		plt.show()
		break
'''
#sys.exit(1)
print("training")
#logistic = linear_model.LogisticRegression()
logistic = svm.SVC(kernel='poly')
rbm = BernoulliRBM(random_state=0, verbose=True)

classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
rbm.learning_rate = 0.06
rbm.n_iter = 20
# More components tend to give better prediction performance, but larger
# fitting time
rbm.n_components = 100
logistic.C = 6000.0

#classifier = svm.SVC(kernel='poly')
#classifier = svm.NuSVC()

#classifier = linear_model.LogisticRegression(n_jobs=-1)

#from sklearn.naive_bayes import MultinomialNB
#classifier = MultinomialNB()

#from sklearn.naive_bayes import GaussianNB
#classifier = GaussianNB()

#from sklearn.ensemble import RandomForestClassifier
#classifier = RandomForestClassifier(n_estimators=50)

#from sklearn.tree import DecisionTreeClassifier
#classifier = DecisionTreeClassifier(max_depth=5)

#from sklearn.neural_network import MLPClassifier
#classifier = MLPClassifier(alpha=1)

#classifier = svm.LinearSVC()
classifier.fit(X_train, y_train)

#print("number of support vectors = " + str(len(classifier.support_vectors_)))

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

X = np.array(imgPixels)
X = brightenTestImage(X)

# reshape the input image to 28 x 28 
X = rgb2gray(X)
X = imresize(X, newshape)
print(X)
plt.imshow(X,cmap='gray')
plt.show()
X = X.flatten()
print(classifier.predict(X))
