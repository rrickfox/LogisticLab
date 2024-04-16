import numpy as np
import copy
import parse

m = np.zeros((10,10))
for line in list(open("../transport_demand.txt"))[1:]:
    x, y, v = line.split(";")
    m[int(x)-1, int(y)-1] = int(v)

m1 = m - m.T
for x, y in np.ndindex((10, 10)):
    m1[x, y] = max(m1[x, y], 0)

# print(m1)
# print(m1.sum())

from utils import lib
import itertools

demand = lib.get_demand()
todo = {i:{} for i in demand}
# todo = np.zeros((10, 10))
for x, y in itertools.combinations(range(1, 11), 2):
    todo[x][y] = max(demand[x].get(y, 0) - demand[y].get(x, 0) , 0)
    todo[y][x] = max(demand[y].get(x, 0)  - demand[x].get(y, 0) , 0)

# print(todo)

dem2 = copy.deepcopy(demand)
with open("temp.txt") as file:
    for line in file.readlines():
        tup = parse.parse("(1, {:d}, {:d}, {:d})\n", line)
        print(tup)
        if tup[2] == 0:
            break
        dem2[tup[0]][tup[1]] -= 1
print(dem2)
dem2mat = np.zeros((10, 10))
for start, ends in dem2.items():
    for end, num in ends.items():
        dem2mat[start-1, end-1] = num

print(dem2mat)