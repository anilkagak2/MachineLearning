import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
 
train = pd.read_csv('train.csv')
trainY = train['label']
trainX = train.drop(['label'], axis=1)

print("shape trainY = " + str(trainY.shape))
print("shape trainX = " + str(trainX.shape))

print("Training the classifier..")
clf = RandomForestClassifier(n_estimators=50)
#scores = cross_val_score(clf, trainX, trainY)
#print scores.mean()
model = clf.fit(trainX, trainY)

print("Reading the test data..")
testX = pd.read_csv('test.csv')

print("shape testX = " + str(testX.shape))
N = testX.shape[0]
predictions = pd.DataFrame(np.arange(1, N+1), columns=['ImageId'])

print("Predicting the labels for the test points...")
predictions['Label'] = model.predict(testX)
predictions.to_csv('predictions_50estimators.csv', index=False)