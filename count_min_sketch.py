import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import random

# Classes
class HashFunction:
    def __init__(self, number_extra_hashing, size_hash_function):
        self._number_extra_hashing = number_extra_hashing
        self._size_hash_function = size_hash_function

    def hash(self, element):
        hash_value = hash(element)
        for _ in range(self._number_extra_hashing):
            hash_value = hash(str(hash_value))
        return hash_value % self._size_hash_function

class countMinSketch:
    def __init__(self, size_hash_function, number_hash_functions):
        self._hash_functions = [new_hash_function(i, size_hash_function) for i in range(number_hash_functions)]
        self._count_min_sketches = [defaultdict(lambda : 0) for _ in range(number_hash_functions)]

    def update(self, element):
        for index, hash_function in enumerate(self._hash_functions):
            self._count_min_sketches[index][hash_function.hash(element)] += 1

    def get(self, element):
        return min([self._count_min_sketches[index][hash_function.hash(element)] for index, hash_function in enumerate(self._hash_functions)])

# Helpers
def new_hash_function(number_extra_hashing, size_hash_function):
    return HashFunction(number_extra_hashing, size_hash_function)
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
for number_hash_functions in range(1, 10):
    results = []
    for size_hash_function in range(1, 100):
        count_min_sketch = countMinSketch(size_hash_function, number_hash_functions)
        for element in elements:
            count_min_sketch.update(element)

        # Counting error
        error_by_key = [ count_min_sketch.get(key) / float(actual[key]) for key in actual.keys()]
        # print size_hash_function, np.mean(error_by_key)
        results.append((size_hash_function, np.mean(error_by_key)))

    plt.plot([a for a,b in results], [b for a,b in results], label=str(number_hash_functions)+' hash functions')

plt.legend(loc=0)
plt.xlabel('Size of Hash function')
plt.ylabel('Mean error over the bins')
plt.title('Evolution of the error of Count-Min-Sketch w.r.t. several hash functions size')
plt.show()
