import numpy as np
from sklearn import (preprocessing, metrics)
from scipy import spatial
import math
import random
import timeit 
import operator
def popCoefficient(x, k=.5):
    return (2/np.pi)*np.arctan((np.pi/2)*k*x)

def calcSimilarity(array1, array2, array1TotalInt = None, array2TotalInt = None, k1 = .5):
    array1 = preprocessing.scale(array1)
    array2 = preprocessing.scale(array2)
    similarity_raw = 1/(1+metrics.mean_squared_error(array1, array2))
    if array1TotalInt and array2TotalInt:
        similarity = similarity_raw*popCoefficient(5*(len(array1)/array1TotalInt)*(len(array2)/array2TotalInt), k1)
        return similarity
    return similarity_raw

def dot_product(v1, v2):
    return sum(map(operator.mul, v1, v2))
def vector_cos(v1, v2, standardize = False):
    if(standardize):
        v1 = preprocessing.scale(v1)
        v2 = preprocessing.scale(v2)
    prod = dot_product(v1, v2)
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    if(len1!=0 and len2!=0):
    	return prod / (len1 * len2)
    else: return 0
 

def scipyCos(u, v):
	return 1 - spatial.distance.cosine(u, v)

u = [random.random() for i in range(100)]
v = [random.random() for i in range(100)]
#print(timeit.timeit('scipyCos(u, v)', number = 10000, setup = "from __main__ import scipyCos, u, v"))
#print(timeit.timeit('calcSimilarity(u, v)', number = 10000, setup = "from __main__ import calcSimilarity, u, v"))
print(timeit.timeit('vector_cos(u, v)', number = 10000, setup = "from __main__ import vector_cos, u, v"))


print(vector_cos([-1, 0, 1], [1, 0, 1]))


