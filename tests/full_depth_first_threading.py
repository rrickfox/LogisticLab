from utils import libpypy as lib
import time, math, copy, traceback, threading

demand_to_tup = lambda a: tuple(sorted([(item[0], tuple(sorted(item[1].items()))) for item in a.items()]))

# visited = {}
# todo = deque([(1, demand_to_tup(demand), 0)]) # (position, demand, distance)

# while todo:
#     position, dem, dist = todo.pop()

#     if (position, dem) in visited and visited[(position, dem)] <= dist:
#         continue
#     visited[(position, dem)] = dist

#     dem_parsed = {item[0]:{item2[0]:item2[1] for item2 in item[1]} for item in dem}


def run(position, dem, dist, last_was_jump, depth, history, thread_index, distances, visited, best, best_history, timeout, start_time, debug):
    # global distances, visited, best
    
    # print(position, dem, dist, last_was_jump, depth)
    
    if time.time() > start_time + timeout: return

    dem_tup = demand_to_tup(dem)
    if (position, dem_tup) in visited and visited[(position, dem_tup)] <= dist:
        return
    visited[(position, dem_tup)] = dist

    if dist >= best[0]:
        return

    # check if best is still possible
    if dist + lib.calculate_lower_bound(dem, distances) >= best[0]:
        return

    if len(dem) == 0 and dist < best[0]:
        best[0] = dist
        best_history[0] = history
        if debug:
            print(str(history)+"\nNew Best:", best, "index:", thread_index, "time:", time.time() - start_time)
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
            run(next_pos, d, dist + distances[position][next_pos], False, depth+1, history + [(1, position, next_pos, 1)], thread_index, distances, visited, best, best_history, timeout, start_time, debug)
            if time.time() > start_time + timeout: return

    if position not in dem or not last_was_jump: # we have to jump when no connection exists from this node, but we can when the last move wasn't a jump
        try:
            for next_pos in sorted([p for p in dem if p != position], key=lambda other, pos=position: (len(dem[other]), -distances[pos][other]), reverse=True):
                if next_pos == position:
                    continue
                # print("Jumping from", position, "to", next_pos)
                run(next_pos, copy.deepcopy(dem), dist + distances[position][next_pos], True, depth+1, history + [(1, position, next_pos, 0)], thread_index, distances, visited, best, best_history, timeout, start_time, debug)
                if time.time() > start_time + timeout: return
        except ValueError:
            traceback.print_exc()
            print(distances, position)

def thread_func(position, dem, dist, last_was_jump, depth, history, thread_index, distances, visited, best, best_history, timeout, start_time, debug):
    return run(position, dem, dist, last_was_jump, depth, history, thread_index, distances, visited, best, best_history, timeout, start_time, debug)

def one_vehicle_dfs_threading(timeout, debug = False):
    start_time = time.time()
    distances = lib.get_distances()
    demand = lib.get_demand()
    
    visited = {}
    best = [math.inf]
    best_history = [[(0, 0)]]

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
            x = threading.Thread(target=thread_func, args=(j, dem2, distances[1][i]+distances[i][j], False, 2, [(1, 1, i, 1), (1, i, j, 1)], (i, j), distances, visited, best, best_history, timeout, start_time, debug), daemon=True)
            threads.append(x)
            x.start()

    for thread in threads:
        thread.join()

    return best[0], best_history[0]


if __name__ == "__main__":
    start_time = time.time()
    ret = one_vehicle_dfs_threading(90, True)
    print(ret)
    print(f"--- {(time.time() - start_time)} seconds ---")