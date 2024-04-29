from utils import lib
import math, time, copy
start_time = time.time()

def jump_lower_bound(num_vehicles = 1, demand = None, positions = None):
    distances = lib.get_distances()

    if demand is None:
        demand = lib.get_demand()
    
    if positions is None:
        positions = [i+1 for i in range(num_vehicles)]

    nodes = {i:[0, 0] for i in range(1, 11)} # ausgehende, eingehende
    for i, endpoints in demand.items():
        nodes[i][0] = sum(endpoints.values())
        for j, num in endpoints.items():
            nodes[j][1] += num

    # print(nodes)
    for i in positions:
        nodes[i][1] += 1

    differences = {i: n1-n2 for i, (n1, n2) in nodes.items()} # neg = mehr eingehende, pos = mehr ausgehende
    # print(differences)
    # print(sum(differences.values()))
    # print(sum(abs(x) for x in differences.values())/2)
    differences = {k: v for k, v in differences.items() if v != 0}

    # quit()

    visited = {}
    best = [math.inf]
    best_history = [[(0, 0)]]
    def run(diff, dist, history, visited, distances, best):
        # global visited, distances, best

        diff_tup = tuple(sorted(diff.items()))
        if diff_tup in visited and visited[diff_tup] <= dist:
            return
        visited[diff_tup] = dist

        if dist >= best[0]:
            return
        
        if sum(x for x in diff.values() if x < 0) == -num_vehicles:
            if dist < best[0]:
                best[0] = dist
                best_history[0] = history
            # print(history)
            # print("New Best:", best)
            # print(f"--- {(time.time() - start_time)} seconds ---")
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
            run(new_diff, dist + distances[start][end], history + [(start, end)], visited, distances, best)

    run(differences, 0, [], visited, distances, best)
    return best[0], best_history[0]

if __name__ == "__main__":
    num_vehicles = 5
    best, _ = jump_lower_bound(num_vehicles)
    demand = lib.get_demand()
    distances = lib.get_distances()
    print("Best:", best / num_vehicles)
    print("Lower bound, only demand", lib.calculate_lower_bound(demand, distances) / num_vehicles)
    print("Lower bound, demand and jumps:", best / num_vehicles + lib.calculate_lower_bound(demand, distances) / num_vehicles)
    print(f"--- {(time.time() - start_time)} seconds ---")