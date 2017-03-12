import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import random

# Classes
class HashFunction:
    def __init__(self, a, b, size_hash_function):
        self._a = a
        self._b = b
        self._size_hash_function = size_hash_function

    def hash(self, element):
        return (((hash(element) + self._a) % self._size_hash_function) + self._b) % self._size_hash_function

class countMinSketch:
    def __init__(self, size_hash_function, number_hash_functions):
        self._hash_functions = [new_hash_function(size_hash_function) for _ in range(number_hash_functions)]
        self._count_min_sketch = defaultdict(lambda : 0)

    def update(self, element):
        for hash_function in self._hash_functions:
            self._count_min_sketch[hash_function.hash(element)] += 1

    def get(self, element):
        return min([self._count_min_sketch[hash_function.hash(element)] for hash_function in self._hash_functions])

# Helpers
def new_hash_function(size_hash_function):
    a, b = random.randint(1, size_hash_function), random.randint(1, size_hash_function)
    print '=>', a, b, size_hash_function
    return HashFunction(a, b, size_hash_function)
#    return HashFunction(1, 0, size_hash_function)

# Script
f = open('data.txt')
actual = defaultdict(lambda : 0)
elements = []
for line in f:
    actual[line] += 1
    elements.append(line)
f.close()

# Count-Min-Sketch
number_hash_functions = 2
results = []
for size_hash_function in range(1, 21):
    count_min_sketch = countMinSketch(size_hash_function, number_hash_functions)
    for element in elements:
        count_min_sketch.update(element)

    # Counting error
    error_by_key = [ count_min_sketch.get(key) / float(actual[key]) for key in actual.keys()]
    print size_hash_function, np.mean(error_by_key)
    results.append((size_hash_function, np.mean(error_by_key)))

plt.plot([a for a,b in results], [b for a,b in results])
plt.xlabel('Size of Hash function')
plt.ylabel('Mean error over the bins')
plt.title('Evolution of the error of Count-Min-Sketch w.r.t. one hash function size')
plt.show()
