import numpy as np
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

FN = raw_input()
x = FN.split()
F = int( x[0] )
N = int( x[1] )
train_X, train_Y = [], []
for _ in range(0, N):
    trainPnt = raw_input()
    trainPnt = trainPnt.strip().split()
    features = [ float(x) for x in trainPnt[:F] ]
    price = float(trainPnt[-1])
    train_X.append(features)
    train_Y.append(price)

T = int( raw_input() )
test_X = []
for _ in range(0, T):
    testPnt = raw_input()
    testPnt = testPnt.strip().split()
    features = [ float(x) for x in testPnt[:F] ]
    test_X.append(features)
    
#print("Training..")
## Train the regressor
#model = linear_model.LinearRegression()
degree = 3
model = make_pipeline(PolynomialFeatures(degree), Ridge())
model.fit(np.array(train_X), np.array(train_Y))

#print("Prediction..")
## Test the regressor
predictions = model.predict(np.array(test_X))
for price in predictions:
    print(price)