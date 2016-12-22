import numpy as np
import sys
lines = sys.stdin.read().strip().split("\n")
vals = [ line.split(" ") for line in lines ]
x = []
for y in vals:
    y = [ [ int(p) for p in u.split(",") ] for u in y ]
    x.append(y)

img = np.array(x)
meanVal = np.mean(img)
#print(meanVal)

numPixels = img.shape[0]*img.shape[1]*img.shape[2]
blackPixels = (img < 50).sum()
#print(numPixels)
#print(blackPixels)
#print(blackPixels *1.0/ numPixels)

#if meanVal < 50:
if (blackPixels *1.0/ numPixels) > 0.4:
    print("night")
else:
    print("day")