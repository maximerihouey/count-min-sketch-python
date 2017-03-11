import string
import random

def new_update(update_size):
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(update_size)])

f = open('data.txt', 'w')

update_size = 2
number_updates = 1000
i = 0
while i < number_updates:
    f.write(new_update(update_size)+'\n')
    i += 1

f.close()
