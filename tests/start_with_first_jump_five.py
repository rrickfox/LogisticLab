import copy
import threading, parse
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

    if max(dists) + lib.calculate_lower_bound(dem, distances) / 5 >= best:
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

num_vehicles = 5

vehicles = {i: (i, 0) for i in range(1, num_vehicles + 1)}

history = []
with open("input_five_vehicles.txt") as file:
    for line in file.readlines():
        tup = parse.parse("({:d}, {:d}, {:d}, {:d})\n", line)
        history.append(tuple(tup))

dist_before_first_jump = [0] * num_vehicles
history_before_first_jump = []
dem2 = copy.deepcopy(demand)
dem3 = {i: {j: 0 for j in range(1, 11)} for i in range(1, 11)}
last_pos = [0] * num_vehicles
last_dist = [0] * num_vehicles
for tup in history:
    if tup[3] == 0:
        break
    last_pos[tup[0] - 1] = tup[2]
    temp = vehicles[tup[0]][1]
    for v_id in vehicles:
        vehicles[v_id] = (vehicles[v_id][0], vehicles[v_id][1] - temp)
    vehicles[tup[0]] = (tup[2], distances[tup[1]][tup[2]])
    # print(vehicles)
    # last_dist[tup[0]-1] = distances[tup[1]][tup[2]]
    dem2[tup[1]][tup[2]] -= 1
    dem3[tup[1]][tup[2]] += 1
    dist_before_first_jump[tup[0]-1] += distances[tup[1]][tup[2]]
    history_before_first_jump.append(tup)

# print(vehicles)
# quit()

new_demands = {}
for i in dem2:
    d = {j: val for j, val in dem2[i].items() if val > 0}
    if len(d) > 0:
        new_demands[i] = d
print(new_demands)

threads = []
vehicle_id, (position, rest_dist) = sorted(vehicles.items(), key=lambda vehic: (vehic[1][1], vehic[0]))[0]
for vehic_id in vehicles:
    vehicles[vehic_id] = (vehicles[vehic_id][0], vehicles[vehic_id][1] - rest_dist)

for i in sorted(filter(lambda other, vehics = vehicles, pos = position: sum(new_demands[other].values()) > sum(v[0] == other for v in  vehics.values()) and other != pos, new_demands), key=lambda other, pos=position: (len(new_demands[other]), -distances[pos][other]), reverse=True):
    v = copy.deepcopy(vehicles)
    v[vehicle_id] = (i, distances[position][i])
    dists2 = copy.deepcopy(dist_before_first_jump)
    dists2[vehicle_id - 1] += distances[position][i]
    l = [False] * num_vehicles
    l[vehicle_id - 1] = True
    
    vehicle_id2, (position2, rest_dist2) = sorted(v.items(), key=lambda vehic: (vehic[1][1], vehic[0]))[0]
    for vehic_id in v:
        v[vehic_id] = (v[vehic_id][0], v[vehic_id][1] - rest_dist2)
    for j in sorted(new_demands[position2], key=lambda other, pos=position2: (len(new_demands.get(other, [])), distances[pos][other]), reverse=True):
        dem = copy.deepcopy(new_demands)
        v1 = copy.deepcopy(v)
        dem[position2][j] -= 1
        if dem[position2][j] == 0:
            dem[position2].pop(j)
        if len(dem[position2]) == 0:
            dem.pop(position2)
        v1[vehicle_id2] = (j, distances[position2][j])
        dists3 = copy.copy(dists2)
        dists3[vehicle_id2 - 1] += distances[position2][j]
        l2 = copy.copy(l)
        l2[vehicle_id2 - 1] = True
        x = threading.Thread(target=thread_func, args=(v1, dem, dists3, l2, 2, history_before_first_jump + [(vehicle_id, position, i, 0), (vehicle_id2, position2, j, 1)]), daemon=True)
        threads.append(x)
        x.start()
        
input()

# run(vehicles, demand, [0, 0, 0, 0, 0], [False, False, False, False, False], 0, [])

print(f"--- {(time.time() - start_time)} seconds ---")