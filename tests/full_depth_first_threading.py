from utils import lib
import time, math, copy, traceback, threading
from collections import deque
start_time = time.time()

distances = lib.get_distances()

demand = lib.get_demand()

demand_to_tup = lambda a: tuple(sorted([(item[0], tuple(sorted(item[1].items()))) for item in a.items()]))

# visited = {}
# todo = deque([(1, demand_to_tup(demand), 0)]) # (position, demand, distance)

# while todo:
#     position, dem, dist = todo.pop()

#     if (position, dem) in visited and visited[(position, dem)] <= dist:
#         continue
#     visited[(position, dem)] = dist

#     dem_parsed = {item[0]:{item2[0]:item2[1] for item2 in item[1]} for item in dem}

visited = {}
best = math.inf
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

def thread_func(position, dem, dist, last_was_jump, depth, history, thread_index):
    return run(position, dem, dist, last_was_jump, depth, history, thread_index)

threads = []
# x = threading.Thread(target=thread_func, args=(1, copy.deepcopy(demand), 0, False, 0, [], 1), daemon=True)
# threads.append(x)
# x.start()
for i in sorted(demand[1], key=lambda other, pos=1: (len(demand.get(other, [])), distances[pos][other]), reverse=True):
    dem = copy.deepcopy(demand)
    dem[1][i] -= 1
    for j in sorted(dem[i], key=lambda other, pos=i: (len(dem.get(other, [])), distances[pos][other]), reverse=True):
        dem2 = copy.deepcopy(dem)
        dem2[i][j] -= 1
        x = threading.Thread(target=thread_func, args=(j, dem2, distances[1][i]+distances[i][j], False, 2, [(1, 1, i, 1), (1, i, j, 1)], (i, j)), daemon=True)
        threads.append(x)
        x.start()

for thread in threads:
    thread.join()

# run(1, demand, 0, False, 0, [])
print(f"--- {(time.time() - start_time)} seconds ---")