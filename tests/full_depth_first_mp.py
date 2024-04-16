from utils import lib
import time, math, copy, traceback
from multiprocessing import Process, Manager


# visited = {}
# todo = deque([(1, demand_to_tup(demand), 0)]) # (position, demand, distance)

# while todo:
#     position, dem, dist = todo.pop()

#     if (position, dem) in visited and visited[(position, dem)] <= dist:
#         continue
#     visited[(position, dem)] = dist

#     dem_parsed = {item[0]:{item2[0]:item2[1] for item2 in item[1]} for item in dem}

# visited = {}
# best = math.inf
def demand_to_tup(a):
    return tuple(sorted([(item[0], tuple(sorted(item[1].items()))) for item in a.items()]))

def run(position, dem, dist, last_was_jump, depth, history, thread_index, distances, visited, best, start_time):
    # global distances, visited, best
    
    # print(position, dem, dist, last_was_jump, depth)

    dem_tup = demand_to_tup(dem)
    if (position, dem_tup) in visited and visited[(position, dem_tup)] <= dist:
        return
    visited[(position, dem_tup)] = dist

    if dist >= best.value:
        return

    # check if best is still possible
    # if depth % 10 == 0:
    if dist + lib.calculate_lower_bound(dem, distances) >= best.value:
        return

    if len(dem) == 0:
        best.value = min(best.value, dist)
        print(str(history)+"\nNew Best:", best.value, "index:", thread_index, "time:", time.time() - start_time)
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
            run(next_pos, d, dist + distances[position][next_pos], False, depth+1, history + [(1, position, next_pos, 1)], thread_index, distances, visited, best, start_time)

    if position not in dem or not last_was_jump: # we have to jump when no connection exists from this node, but we can when the last move wasn't a jump
        try:
            for next_pos in sorted([p for p in dem if p != position], key=lambda other, pos=position: (len(dem[other]), -distances[pos][other]), reverse=True):
                if next_pos == position:
                    continue
                # print("Jumping from", position, "to", next_pos)
                run(next_pos, copy.deepcopy(dem), dist + distances[position][next_pos], True, depth+1, history + [(1, position, next_pos, 0)], thread_index, distances, visited, best, start_time)
        except ValueError:
            traceback.print_exc()
            print(distances, position)

def mp_func(position, dem, dist, last_was_jump, depth, history, thread_index, distances, visited, best, start_time):
    return run(position, dem, dist, last_was_jump, depth, history, thread_index, distances, visited, best, start_time)

if __name__ == "__main__":
    start_time = time.time()

    distances = lib.get_distances()

    demand = lib.get_demand()

    m = Manager()
    best = m.Value("d", math.inf)
    visited = m.dict()

    # threads = []
    # x = threading.Thread(target=thread_func, args=(1, copy.deepcopy(demand), 0, False, 0, [], 1), daemon=True)
    # threads.append(x)
    # x.start()
    # for i in sorted(demand[1], key=lambda other, pos=1: (len(demand.get(other, [])), distances[pos][other]), reverse=True):
    #     dem = copy.deepcopy(demand)
    #     dem[1][i] -= 1
    #     x = threading.Thread(target=thread_func, args=(i, dem, distances[1][i], False, 1, [(1, 1, i, 1)], i), daemon=True)
    #     threads.append(x)
    #     x.start()

    # for thread in threads:
    #     thread.join()

    processes = []
    p = Process(target=mp_func, args=(1, copy.deepcopy(demand), 0, False, 0, [], 1, distances, visited, best, start_time))
    processes.append(p)
    p.start()
    for i in sorted(demand[1], key=lambda other, pos=1: (len(demand.get(other, [])), distances[pos][other]), reverse=True):
        dem = copy.deepcopy(demand)
        dem[1][i] -= 1
        p = Process(target=mp_func, args=(i, dem, distances[1][i], False, 1, [(1, 1, i, 1)], i, distances, visited, best, start_time), daemon=True)
        processes.append(p)
        p.start()
    
    input()

    for p in processes:
        p.kill()

    # run(1, demand, 0, False, 0, [])
    print(f"--- {(time.time() - start_time)} seconds ---")