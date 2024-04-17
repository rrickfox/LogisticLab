import copy
import parse, time, math, traceback, threading
from utils import libpypy as lib

distances = lib.get_distances()
demand = lib.get_demand()

dist_before_first_jump = 0
history_before_first_jump = []
dem_after_jump = copy.deepcopy(demand)
dem_before_jump = {i: {j: 0 for j in range(1, 11)} for i in range(1, 11)}
jumps = {}
with open("input_16156.txt") as file:
    for line in file.readlines():
        # print(line)
        tup = parse.parse("(1, {:d}, {:d}, {:d})\n", line)
        # print(tup)
        # if tup[2] == 0:
        #     break
        # dem_after_jump[tup[0]][tup[1]] -= 1
        # dem_before_jump[tup[0]][tup[1]] += 1
        # dist_before_first_jump += distances[tup[0]][tup[1]]
        # history_before_first_jump.append((1, tup[0], tup[1], tup[2]))
        if tup[2] == 0:
            jumps[(tup[0], tup[1])] = jumps.get((tup[0], tup[1]), 0) + 1

print(dict(sorted(jumps.items())))