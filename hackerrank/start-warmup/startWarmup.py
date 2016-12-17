import numpy as np
import math
import scipy.stats as stats

N = int(raw_input())
numbers = raw_input().strip().split()
A = [ int(x) for x in numbers ]
A = np.array(A)
mu = np.mean(A)
print("{0:0.1f}".format(mu))

print("{0:0.1f}".format(np.median(A)))

counts = np.bincount(A)
print(np.argmax(counts))

sigma = np.std(A)
print("{0:0.1f}".format(sigma))

Q = 0.95
margin_of_error = sigma/math.sqrt(N)
confidence_interval = (mu - 1.96* margin_of_error, mu + 1.96*margin_of_error)
print("{0:0.1f} {1:0.1f}".format(confidence_interval[0], confidence_interval[1]))
