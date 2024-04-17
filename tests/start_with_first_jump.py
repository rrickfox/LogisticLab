# import numpy as np
import copy
import parse, time, math, traceback, threading
from utils import libpypy as lib

distances = lib.get_distances()
demand = lib.get_demand()

dist_before_first_jump = 0
history_before_first_jump = []
dem2 = copy.deepcopy(demand)
dem3 = {i: {j: 0 for j in range(1, 11)} for i in range(1, 11)}
with open("input_16200.txt") as file:
    for line in file.readlines():
        tup = parse.parse("(1, {:d}, {:d}, {:d})\n", line)
        if tup[2] == 0:
            break
        dem2[tup[0]][tup[1]] -= 1
        dem3[tup[0]][tup[1]] += 1
        dist_before_first_jump += distances[tup[0]][tup[1]]
        history_before_first_jump.append((1, tup[0], tup[1], tup[2]))
# print(dem2)
print(dist_before_first_jump)

# dem2mat = np.zeros((10, 10))
# for start, ends in dem2.items():
#     for end, num in ends.items():
#         dem2mat[start-1, end-1] = num
# print(dem2mat.sum())

# print(dem2mat)

new_demands = {}
for i in dem2:
    d = {j: val for j, val in dem2[i].items() if val > 0}
    if len(d) > 0:
        new_demands[i] = d
print(new_demands)
new_demands_before_jump = {}
for i in dem3:
    d = {j: val for j, val in dem3[i].items() if val > 0}
    if len(d) > 0:
        new_demands_before_jump[i] = d
print(new_demands_before_jump)

start_time = time.time()

visited = {}
best = math.inf

demand_to_tup = lambda a: tuple(sorted([(item[0], tuple(sorted(item[1].items()))) for item in a.items()]))
def run(position, dem, dist, last_was_jump, depth, history, thread_index):
    global distances, visited, best
    
    # print(position, dem, dist, last_was_jump, depth)

    dem_tup = demand_to_tup(dem)
    if (position, dem_tup) in visited and visited[(position, dem_tup)] <= dist:
        return
    visited[(position, dem_tup)] = dist

    if dist >= best:
        return

    # check if best is still possible
    # if depth % 10 == 0:
    if dist + lib.calculate_lower_bound(dem, distances) >= best:
        return

    if len(dem) == 0:
        best = min(best, dist)
        print(str(history)+"\nNew Best:", best, "index:", thread_index, "time:", time.time() - start_time)
        # print(history)
        # print("New Best:", best)
        # print(f"--- {(time.time() - start_time)} seconds ---")
        return

    # print(position, dem, dist, last_was_jump, depth)
    if position in dem:
        for next_pos in sorted(dem[position], key=lambda other, pos=position: (len(dem.get(other, [])), distances[pos][other]), reverse=True):
            if next_pos == position:
                continue
            d = copy.deepcopy(dem)
            d[position][next_pos] -= 1
            if d[position][next_pos] == 0:
                d[position].pop(next_pos)
            if len(d[position]) == 0:
                d.pop(position)

            # print("Going from", position, "to", next_pos)
            run(next_pos, d, dist + distances[position][next_pos], False, depth+1, history + [(1, position, next_pos, 1)], thread_index)

    if position not in dem or not last_was_jump: # we have to jump when no connection exists from this node, but we can when the last move wasn't a jump
        try:
            for next_pos in sorted([p for p in dem if p != position], key=lambda other, pos=position: (len(dem[other]), -distances[pos][other]), reverse=True):
                if next_pos == position:
                    continue
                # print("Jumping from", position, "to", next_pos)
                run(next_pos, copy.deepcopy(dem), dist + distances[position][next_pos], True, depth+1, history + [(1, position, next_pos, 0)], thread_index)
        except ValueError:
            traceback.print_exc()
            print(distances, position)

# demand[1][8] -= 1
# run(9, new_demands, dist_before_first_jump, False, 1, history_before_first_jump)

def thread_func(position, dem, dist, last_was_jump, depth, history, thread_index):
    return run(position, dem, dist, last_was_jump, depth, history, thread_index)

threads = []
# x = threading.Thread(target=thread_func, args=(1, copy.deepcopy(demand), 0, False, 0, [], 1), daemon=True)
# threads.append(x)
# x.start()
for i in sorted([p for p in new_demands if p != 9], key=lambda other, pos=9: (len(new_demands[other]), -distances[pos][other]), reverse=True):
    dem = copy.deepcopy(new_demands)
    x = threading.Thread(target=thread_func, args=(i, dem, dist_before_first_jump + distances[9][i], False, 1, history_before_first_jump + [(1, 9, i, 0)], i), daemon=True)
    threads.append(x)
    x.start()

input()
print(f"--- {(time.time() - start_time)} seconds ---")