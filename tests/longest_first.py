from utils import lib
import time
start_time = time.time()

distances = lib.get_distances()

demand = lib.get_demand()

# print(demand)

position = 1
history = []
while demand:
    # print(demand)
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
        history.append((1, position, next_pos, 1))
        position = next_pos
        # print(demand)
    else: # no job available, jump to next machine
        # next_pos = sorted(demand, key=lambda other: len(demand[other]), reverse=True)[0] # jump to node with most demand (only nodes, not count)
        next_pos = sorted(demand, key=lambda other, pos=position: (len(demand[other]), -distances[pos][other]), reverse=True)[0] # jump to node with most demand (only nodes, not count), when more than one possible, use least distance
        # next_pos = sorted(demand, key=lambda other: sum(demand[other].values()), reverse=True)[0] # jump to node with most demand (only nodes, not count)
        # next_pos = sorted(demand, key=lambda other, pos=position: distances[pos][other])[0] # jump to nearest
        # print("jumping to:", next_pos)
        history.append((1, position, next_pos, 0))
        position = next_pos

print(len(history))
print(history)

lib.write_history("schedule_longest_first", history)

print(f"--- {(time.time() - start_time)} seconds ---")