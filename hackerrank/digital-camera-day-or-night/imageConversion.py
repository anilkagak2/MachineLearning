from scipy.ndimage import imread 
import numpy as np
import sys

if len(sys.argv) != 3:
    print("invalid arguments")
    sys.exit(1)

imageFile = sys.argv[1]
outFile = sys.argv[2]

x = imread(imageFile)
print(x.shape[:2])
r,c = x.shape[:2]
with open(outFile, 'w') as fp:
    for i in range(r):
        line = " ".join( [ ",".join([str(u) for u in x[i][j]])  for j in range(c)] )
        fp.write(line + "\n")

#x.tofile(outFile,sep=',',format='%10.5f')
