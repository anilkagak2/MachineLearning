import numpy as np
from scipy import ndimage, misc
from scipy.ndimage import uniform_filter
from sklearn.feature_extraction import image
from matplotlib import pyplot as plt
from numpy.linalg import norm
import sys

newshape = (56,22)
#newshape = (10,10)

def rgb2gray(rgb):
  return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

def hog_feature(im):  
  # convert rgb to grayscale if needed
  if im.ndim == 3:
    I = rgb2gray(im)
  else:
    I = np.atleast_2d(im)

  sx, sy = I.shape # image size
  orientations = 9 # number of gradient bins
  cx, cy = (8, 8) # pixels per cell

  gx = np.zeros(I.shape)
  gy = np.zeros(I.shape)
  gx[:, :-1] = np.diff(I, n=1, axis=1) # compute gradient on x-direction
  gy[:-1, :] = np.diff(I, n=1, axis=0) # compute gradient on y-direction
  grad_mag = np.sqrt(gx ** 2 + gy ** 2) # gradient magnitude
  grad_ori = np.arctan2(gy, (gx + 1e-15)) * (180 / np.pi) + 90 # gradient orientation

  n_cellsx = int(np.floor(sx / cx))  # number of cells in x
  n_cellsy = int(np.floor(sy / cy))  # number of cells in y
  # compute orientations integral images
  orientation_histogram = np.zeros((n_cellsx, n_cellsy, orientations))
  for i in range(orientations):
    # create new integral image for this orientation
    # isolate orientations in this range
    temp_ori = np.where(grad_ori < 180 / orientations * (i + 1),
                        grad_ori, 0)
    temp_ori = np.where(grad_ori >= 180 / orientations * i,
                        temp_ori, 0)
    # select magnitudes for those orientations
    cond2 = temp_ori > 0
    temp_mag = np.where(cond2, grad_mag, 0)
    print(temp_mag.shape)
    print(cx)
    print(cy)
    orientation_histogram[:,:,i] = uniform_filter(temp_mag, size=(cx, cy))[cx/2::cx, cy/2::cy].T
  
  return orientation_histogram.ravel()

digitsImage = misc.imread('digits.jpg')
digits = {}
features = {}
numDigits = 10
for i in range(numDigits):
	digit = digitsImage[27:80, 20+i*50:20+(i+1)*50]
	digit = digit < digit.mean()
	#digit = misc.imresize(digit, (57, 34))
	#plt.imshow(digit, cmap='gray')
	#plt.show()
	
	rs, cs = np.where(digit > 0)
	topr, bottomr = min(rs), max(rs)
	leftc, rightc = min(cs), max(cs)
	cropped = digit[topr:bottomr, leftc:rightc]
	cropped = misc.imresize(cropped, newshape)
	#plt.imshow(cropped, cmap='gray')
	#plt.show()
	digits[i] = cropped
	#y = hog_feature(cropped)
	mask = cropped.astype(bool)
	#y = image.img_to_graph(cropped, mask=mask)
	y = image.img_to_graph(cropped)
	#print(y)
	#plt.imshow(y, cmap='gray')
	#plt.show()
	features[i] = y
	print(cropped.shape)
	
#plt.imshow(digits[3], cmap='gray')
#plt.show()

print(features[1])

print("test image")
lines = sys.stdin.read().strip().split("\n")
vals = [ line.split(" ") for line in lines[1:] ]
imgPixels = []
for y in vals:
    y = [ [ int(p) for p in u.split(",") ] for u in y ]
    imgPixels.append(y)
	
X = np.array(imgPixels)
X = rgb2gray(X)
plt.imshow(X)
plt.show()
X = ndimage.filters.gaussian_filter(X, 3) 

X, num_cm = ndimage.label(X)
print(num_cm)
X = misc.imresize(X, newshape)
print(X.shape)

mask = X.astype(bool)
#y = image.img_to_graph(X, mask=mask)
y = image.img_to_graph(X)
print(y)
plt.imshow(X, cmap='gray')
plt.show()

y = y.toarray().flatten()
for i in range(numDigits):
	ft = features[i].toarray().flatten()
	#dist = norm((ft*y))
	dist = y.dot(ft)
	
	print(dist)
