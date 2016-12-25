import numpy as np
from scipy.ndimage import imread 
from matplotlib import pyplot as plt
import sys
import os
import json
import pickle

imgTemplates = {}

for i in range(25):
    featuresFile = os.path.join("input", "input" + ("%02d" % (i,)) + ".jpg")
    targetsFile =  os.path.join("output", "output" + ("%02d" % (i,)) + ".txt")
    x = imread(featuresFile)
    x[x > 50] = 255
    x = x[7:-7, 5:-10, :]
    #plt.imshow(x)
    #plt.show()

    targets = open(targetsFile).read().strip()
    print(targets)
    print(featuresFile)
    
    j = 0
    for char in targets:
        template = x[:, j:j+9, :]
        #print(char)
        #plt.imshow(template)
        #plt.show()
        '''
        if char in imgTemplates:
            imgTemplates[char].append(template)
        else:
            imgTemplates[char] = [template]
        '''
        imgTemplates[char] = template
        j += 9


print("JSON Dictionary writing")
U = pickle.dumps(imgTemplates)
#U = str(imgTemplates)
print(len(U))

import base64
Ubase64 = base64.b64encode(U)
with open("modelbase64.txt", "wb") as fp:
    fp.write(U)

with open("model.txt", "wb") as fp:
    fp.write(U)

#from ast import literal_eval
#imgTemplates = literal_eval(U)
imgTemplates = pickle.loads(U)

print("test image")
#featuresFile = os.path.join("input", "input" + ("%02d" % (0,)) + ".jpg")
#x = imread(featuresFile)
featuresFile = os.path.join("input", "input" + ("%02d" % (0,)) + ".txt")
lines = open(featuresFile).read().strip().split("\n")
vals = [ line.split(" ") for line in lines[1:] ]
imgPixels = []
for y in vals:
    y = [ [ int(p) for p in u.split(",") ] for u in y ]
    imgPixels.append(y)

x = np.array(imgPixels)
#print (x.shape)

x[x > 50] = 255             # remove gray background
x = x[7:-7, 5:-10, :]       # only keep the pixels

result = ""
j = 0
for i in range(5):
    template = x[:, j:j+9, :]
    j += 9
    
    minDistance = 1000000
    matchedChar = "A"
    for char in imgTemplates:
        charTemplate = imgTemplates[char]
        dist = np.linalg.norm(template - charTemplate)
        if dist < minDistance:
            matchedChar = char
            minDistance = dist

    result += matchedChar

print(result)