import copy
import threading
from utils import libpypy as lib
import time, math
start_time = time.time()

distances = lib.get_distances()

demand = lib.get_demand()

demand_to_tup = lambda a: tuple(sorted([(item[0], tuple(sorted(item[1].items()))) for item in a.items()]))

visited = {}
best = math.inf

def run(vehicles, dem, dists, last_was_jump, depth, history):
    global distances, visited, best
    
    dem_tup = demand_to_tup(dem)
    vehic_tup = tuple(sorted(vehicles.items(), key=lambda vehic: vehic[0]))
    if (vehic_tup, dem_tup) in visited and visited[(vehic_tup, dem_tup)] <= max(dists):
        return
    visited[(vehic_tup, dem_tup)] = max(dists)

    if max(dists) >= best:
        return

    if max(dists) + lib.calculate_lower_bound(dem, distances) / 10 >= best:
        return
    
    if len(dem) == 0:
        best = min(best, max(dists))
        print(history)
        print("New Best:", best)
        print(f"--- {(time.time() - start_time)} seconds ---")
        return
    
    vehicle_id, (position, rest_dist) = sorted(vehicles.items(), key=lambda vehic: (vehic[1][1], vehic[0]))[0]
    for vehic_id in vehicles:
        vehicles[vehic_id] = (vehicles[vehic_id][0], vehicles[vehic_id][1] - rest_dist)
    
    if position in dem: # check if current machine has more jobs
        # select the one with the biggest distance
        for next_pos in sorted(dem[position], key=lambda other, pos=position: (len(dem.get(other, [])), distances[pos][other]), reverse=True): # node with most demand, then most distance
            # print("==========")
            # print(dem)
            # print("vehic", vehicle_id, "position", position, "next pos:", next_pos)
            if next_pos == position:
                continue
            d = copy.deepcopy(dem)
            d[position][next_pos] -= 1
            if d[position][next_pos] == 0:
                d[position].pop(next_pos)
            if len(d[position]) == 0:
                d.pop(position)
            # print(d)
            
            # move
            v = copy.deepcopy(vehicles)
            v[vehicle_id] = (next_pos, distances[position][next_pos])
            dists2 = copy.copy(dists)
            dists2[vehicle_id - 1] += distances[position][next_pos]
            l = copy.copy(last_was_jump)
            l[vehicle_id - 1] = True
            run(v, d, dists2, l, depth + 1 , history + [(vehicle_id, position, next_pos, 1)])

    if position not in dem or not last_was_jump[vehicle_id - 1]: # no job available, jump to next machine
        possible_next = sorted(filter(lambda other, vehics = vehicles, pos = position: sum(dem[other].values()) > sum(v[0] == other for v in  vehics.values()) and other != pos, dem), key=lambda other, pos=position: (len(dem[other]), -distances[pos][other]), reverse=True) # jump to node with most demand (only nodes, not count), when more than one possible, use least distance
        
        if len(possible_next) == 0:
            v = copy.deepcopy(vehicles)
            v[vehicle_id] = (0, math.inf)
            run(v, copy.deepcopy(dem), copy.copy(dists), copy.copy(last_was_jump), depth, history + [])
        
        for next_pos in possible_next:
            v = copy.deepcopy(vehicles)
            v[vehicle_id] = (next_pos, distances[position][next_pos])
            dists2 = copy.deepcopy(dists)
            dists2[vehicle_id - 1] += distances[position][next_pos]
            l = copy.copy(last_was_jump)
            l[vehicle_id - 1] = True
            run(v, copy.deepcopy(dem), dists2, l, depth + 1 , history + [(vehicle_id, position, next_pos, 0)])

def thread_func(vehicles,dem,dists,last_was_jump,depth,history):
    run(vehicles,dem,dists,last_was_jump,depth,history)

vehicles = {i: (i, 0) for i in range(1, 11)}

threads = []
for i in range(1, 11): # start with each vehicle
    for j in sorted(demand[i], key=lambda other, pos=i: (len(demand.get(other, [])), distances[pos][other]), reverse=True):
        dem = copy.deepcopy(demand)
        v1 = copy.deepcopy(vehicles)
        dem[i][j] -= 1
        if dem[i][j] == 0:
            dem[i].pop(j)
        if len(dem[i]) == 0:
            dem.pop(i)
        v1[i] = (j, distances[i][j])
        d = [0] * 10
        d[i - 1] = distances[i][j]
        x = threading.Thread(target=thread_func, args=(v1, dem, d, [False] * 10, 1, [(i, i, j, 1)]), daemon=True)
        threads.append(x)
        x.start()
        
input()

# run(vehicles, demand, [0, 0, 0, 0, 0], [False, False, False, False, False], 0, [])

print(f"--- {(time.time() - start_time)} seconds ---")