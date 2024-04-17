import math, json

def euclid_dist(a1, b1, a2, b2):
    return math.sqrt((a1 - a2)**2 + (b1 - b2)**2)

def pretty_print(obj) -> None:
    print(json.dumps(obj, indent=2))

def get_distances():
    with open("../machine_positions.txt") as file:
        positions = {int(a[0]): (int(a[1]), int(a[2])) for line in file.readlines()[1:] if (a := line.split(";"))}

    distances = {}
    for index, pos in positions.items():
        distances[index] = {index2: euclid_dist(*pos, *pos2) for index2, pos2 in positions.items() if index2 != index}

    return distances

def get_demand():
    with open("../transport_demand.txt") as file:
        demand = {}
        for line in file.readlines()[1:]:
            a = line.split(";")
            if int(a[2]) != 0:
                if int(a[0]) not in demand:
                    demand[int(a[0])] = {}
                demand[int(a[0])][int(a[1])] = int(a[2])
    return demand

def write_history(name, history):
    with open(f"../{name}.txt", "w") as file:
        file.write("VehicleId;Location;unload;load\n")
        for move, prev_move in zip(history, [(0,0,0,0)]+history[:-1]):
            # print(move, prev_move)
            if move[3] == 1:
                if prev_move[3] == 1:
                    tup = (move[0], move[1], 1, 1) # when moving now and moving before, unload and then load again
                else:
                    tup = (move[0], move[1], 0, 1) # no need to unload when teleporting before
            else:
                if prev_move[3] == 1:
                    tup = (prev_move[0], prev_move[2], 1, 0) # unload from previous
            file.write(";".join(map(str, tup)) + "\n")
        file.write(f"{history[-1][0]};{history[-1][2]};{history[-1][3]};0")

def calculate_lower_bound(demand, distances):
    return sum(sum(distances[start][end] * num for end, num in item.items()) for start, item in demand.items())

def test():
    return "yeah"