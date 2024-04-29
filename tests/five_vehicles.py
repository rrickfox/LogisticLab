from utils import lib
import time, math
start_time = time.time()

distances = lib.get_distances()

demand = lib.get_demand()

# print(demand)

vehicles = {i: (i, 0) for i in range(1, 6)}
history = []
dists = [0, 0, 0, 0, 0]
while demand:
    # select vehicle
    vehicle_id, (position, rest_dist) = sorted(vehicles.items(), key=lambda vehic: (vehic[1][1], vehic[0]))[0]
    for vehic_id in vehicles:
        vehicles[vehic_id] = (vehicles[vehic_id][0], vehicles[vehic_id][1] - rest_dist)
    
    # vehicle is at position
    if position in demand: # check if current machine has more jobs
        # select the one with the biggest distance
        # next_pos = sorted(demand[position], key=lambda other, pos=position: distances[pos][other], reverse=True)[0] # node with most distance to current
        next_pos = sorted(demand[position], key=lambda other, pos=position: (len(demand.get(other, [])), distances[pos][other]), reverse=True)[0] # node with most demand, then most distance
        # print("next pos:", next_pos)
        demand[position][next_pos] -= 1
        if demand[position][next_pos] == 0:
            demand[position].pop(next_pos)
        if len(demand[position]) == 0:
            demand.pop(position)
        
        # move
        history.append((vehicle_id, position, next_pos, 1))
        vehicles[vehicle_id] = (next_pos, distances[position][next_pos])
        dists[vehicle_id - 1] += distances[position][next_pos]
        # position = next_pos
        # print(demand)
    else: # no job available, jump to next machine
        # next_pos = sorted(demand, key=lambda other: len(demand[other]), reverse=True)[0] # jump to node with most demand (only nodes, not count)
        possible_next = sorted(filter(lambda other, vehics = vehicles: sum(demand[other].values()) > sum(v[0] == other for v in  vehics.values()), demand), key=lambda other, pos=position: (len(demand[other]), -distances[pos][other]), reverse=True) # jump to node with most demand (only nodes, not count), when more than one possible, use least distance
        
        if len(possible_next) == 0:
            vehicles[vehicle_id] = (0, math.inf)
            continue
        
        next_pos = possible_next[0]
        # next_pos = sorted(demand, key=lambda other: sum(demand[other].values()), reverse=True)[0] # jump to node with most demand (only nodes, not count)
        # next_pos = sorted(demand, key=lambda other, pos=position: distances[pos][other])[0] # jump to nearest
        # print("jumping to:", next_pos)
        history.append((vehicle_id, position, next_pos, 0))
        vehicles[vehicle_id] = (next_pos, distances[position][next_pos])
        dists[vehicle_id - 1] += distances[position][next_pos]
        # position = next_pos

print(len(history))
print(history)
print(max(dists))

lib.write_history("schedule_longest_first_five_vehicle", history)

print(f"--- {(time.time() - start_time)} seconds ---")