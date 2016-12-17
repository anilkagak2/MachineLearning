import numpy as np
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.preprocessing import Normalizer, PolynomialFeatures
from sklearn.pipeline import make_pipeline

train_X, train_Y = [], []
with open("trainingdata.txt") as fp:
    for line in fp:
        trainPnt = line
        trainPnt = trainPnt.strip().split(',')
        #print(trainPnt)
        if len(trainPnt) != 2: break
        features =  [ float(trainPnt[0]) ]
        price = float(trainPnt[-1])
        train_X.append(features)
        train_Y.append(price)
    
#print("Training..")
## Train the regressor
#model = linear_model.LinearRegression()
degree = 4
#model = make_pipeline(PolynomialFeatures(degree), Ridge())
#model = Ridge())
#model.fit(np.array(train_X), np.array(train_Y))

#print("Prediction..")
test_X = []
testPnt = raw_input()
features = float(testPnt.strip())
test_X.append(features)
## Test the regressor
#predictions = model.predict(np.array(test_X).reshape(1,-1))
predictions = []
for x in test_X:
    if x >= 4.0: print(8.00)
    else: print(2*x)
#for price in predictions:
#    print(price)