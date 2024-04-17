from utils import lib
import math, time, copy
start_time = time.time()

distances = lib.get_distances()

demand = lib.get_demand()

nodes = {i:[0, 0] for i in demand} # ausgehende, eingehende
for i, endpoints in demand.items():
    nodes[i][0] = sum(endpoints.values())
    for j, num in endpoints.items():
        nodes[j][1] += num

print(nodes)
nodes[1][1] += 1

differences = {i: n1-n2 for i, (n1, n2) in nodes.items()} # neg = mehr eingehende, pos = mehr ausgehende
print(differences)
print(sum(differences.values()))
print(sum(abs(x) for x in differences.values())/2)
differences = {k: v for k, v in differences.items() if v != 0}

# quit()

visited = {}
best = math.inf
def run(diff, dist, history):
    global visited, distances, best

    diff_tup = tuple(sorted(diff.items()))
    if diff_tup in visited and visited[diff_tup] <= dist:
        return
    visited[diff_tup] = dist

    if dist >= best:
        return
    
    if sum(x for x in diff.values() if x < 0) == -1:
        best = min(best, dist)
        print(history)
        print("New Best:", best)
        print(f"--- {(time.time() - start_time)} seconds ---")
        return
    
    start = [i for i, num in diff.items() if num < 0][0]
    for end in [i for i, num in diff.items() if num > 0]:
        # print(start, end)
        new_diff = copy.copy(diff)
        new_diff[start] += 1
        if new_diff[start] == 0:
            new_diff.pop(start)
        new_diff[end] -= 1
        if new_diff[end] == 0:
            new_diff.pop(end)
        run(new_diff, dist + distances[start][end], history + [(start, end)])

run(differences, 0, [])
print("Best:", best)
print("Lower bound, only demand", lib.calculate_lower_bound(demand, distances))
print("Lower bound, demand and jumps:", best + lib.calculate_lower_bound(demand, distances))
print(f"--- {(time.time() - start_time)} seconds ---")