from bisect import bisect_left
from time import time


def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)   
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end



# import random
# setTime = 0
# linTime = 0

# for count in range(1000):
# 	s = time()
# 	set1 = set([random.randint(0, 1000) for i in range(1000)])
# 	set2 = set([random.randint(0, 1000) for i in range(1000)])
# 	e = time()
# 	print(e-s)
# 	s = time()
# 	list1 = list((random.randint(0, 1000) for i in range(1000)))
# 	list2 = list((random.randint(0, 1000) for i in range(1000)))
# 	list3 = []
# 	e = time()
# 	print(e-s)
# 	s = time()
# 	difference = set1.difference(set2)
# 	# print(difference)
# 	e = time()
# 	# print(e-s)
# 	setTime += e-s
# 	s = time()
# 	for el in list1:
# 		if el not in list2:
# 			list3.append(el)

# 	e = time()
# 	# print(e-s)
# 	linTime += e-s
# print(setTime)
# print(linTime)