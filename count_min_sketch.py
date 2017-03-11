import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

class countMinSketch:
    def __init__(self, size_hash_function, number_hash_functions):
        self._size_hash_function = size_hash_function
        self._number_hash_functions = number_hash_functions
        self._count_min_sketch = defaultdict(lambda : 0)

    def update(self, element):
        self._count_min_sketch[hash(element) % self._size_hash_function] += 1

    def get(self, element):
        return self._count_min_sketch[hash(element) % self._size_hash_function]

f = open('data.txt')
actual = defaultdict(lambda : 0)
elements = []
for line in f:
    actual[line] += 1
    elements.append(line)
f.close()

# Count-Min-Sketch
number_hash_functions = 1
results = []
for size_hash_function in range(1, 100):
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
