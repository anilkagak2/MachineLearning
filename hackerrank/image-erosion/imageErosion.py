import numpy as np
import cv2

A = [
        [0,0,0,0,0,0,0,0,0,0], 
        [0,1,1,1,1,1,1,1,0,0], 
        [0,0,0,0,1,1,1,1,0,0], 
        [0,0,0,0,1,1,1,1,0,0], 
        [0,0,0,1,1,1,1,1,0,0], 
        [0,0,0,0,1,1,1,1,0,0], 
        [0,0,0,1,1,0,0,0,0,0], 
        [0,0,0,0,0,0,0,0,0,0], 
        [0,0,0,0,0,0,0,0,0,0], 
    ]

img = np.array(A).astype(np.float32)
#print(img.shape)
dilation = np.ones((3, 3))
img = cv2.erode(img, dilation)
print(np.count_nonzero(img))