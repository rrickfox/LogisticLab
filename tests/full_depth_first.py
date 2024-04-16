from utils import lib
import time, math, copy, traceback
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
def run(position, dem, dist, last_was_jump, depth, history):
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
        print(history)
        print("New Best:", best)
        print(f"--- {(time.time() - start_time)} seconds ---")
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
            run(next_pos, d, dist + distances[position][next_pos], False, depth+1, history + [(1, position, next_pos, 1)])

    if position not in dem or not last_was_jump: # we have to jump when no connection exists from this node, but we can when the last move wasn't a jump
        try:
            for next_pos in sorted([p for p in dem if p != position], key=lambda other, pos=position: (len(dem[other]), -distances[pos][other]), reverse=True):
                if next_pos == position:
                    continue
                # print("Jumping from", position, "to", next_pos)
                run(next_pos, copy.deepcopy(dem), dist + distances[position][next_pos], True, depth+1, history + [(1, position, next_pos, 0)])
        except ValueError:
            traceback.print_exc()
            print(distances, position)
demand[1][8] -= 1
run(8, demand, distances[1][8], False, 1, [(1, 1, 8, 1)])
print(f"--- {(time.time() - start_time)} seconds ---")