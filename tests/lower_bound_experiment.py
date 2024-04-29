import copy
import math
from lower_bound_test import jump_lower_bound
from utils import lib

num_vehicles = 5

distances = lib.get_distances()
demand = lib.get_demand()

count_dist_demand = {}
count_complete = {}
for start in demand:
    for end in demand[start]:
        d = distances[start][end]
        count_dist_demand[d] = count_dist_demand.get(d, 0) + demand[start][end]
        count_complete[d] = count_complete.get(d, 0) + demand[start][end]

count_dist_demand = dict(sorted(count_dist_demand.items()))
# print(count_dist_demand)

count_dist_jumps = {}
for start, end in jump_lower_bound(num_vehicles)[1]:
    d = distances[start][end]
    count_dist_jumps[d] = count_dist_jumps.get(d, 0) + demand[start][end]
    count_complete[d] = count_complete.get(d, 0) + demand[start][end]

count_dist_jumps = dict(sorted(count_dist_jumps.items()))
count_complete = dict(sorted(count_complete.items()))
# print(count_dist_jumps)

# print(count_complete)
distributed_total = 0
todo = []
for i in list(count_complete.keys()):
    distributed_total += count_complete[i] // 5 * i
    count_complete[i] = count_complete[i] % num_vehicles
    todo += [i] * count_complete[i]
    if count_complete[i] == 0:
        count_complete.pop(i)

todo.sort(reverse=True)
print(count_complete)
# print(todo)
print(sum(count_complete.values()), "rest total")
print("distributed total", distributed_total)
expected_value = sum(todo) / num_vehicles

best = math.inf
def run(todo, buckets):
    global best

    if len(todo) == 0:
        mse = sum((b_val - expected_value)**2 for b_val in buckets) / num_vehicles
        if mse < best:
            print("New best:", mse)
            print("lower bound", distributed_total + max(buckets))
            print(buckets)
            best = mse
        return

    # if max(buckets) > ((sum(todo) / (num_vehicles - 1)) + min(buckets)) * 0.5:
    #     return

    n = todo.pop()
    for i, _ in sorted(enumerate(buckets), key=lambda x: x[1]):
        b = copy.copy(buckets)
        b[i] += n
        run(copy.copy(todo), b)

run(copy.copy(todo), [0] * num_vehicles)