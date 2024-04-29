from utils import lib

demand = lib.get_demand()

def main():
    n = 10
    g = [[0] * n for _ in range(n)]
    
    # Reading the graph in the adjacency matrix
    print("Enter the adjacency matrix:")
    for i in range(n):
        g[i] = [demand[i+1].get(j+1, 0) for j in range(n)]

    deg = [0] * n
    for i in range(n):
        for j in range(n):
            deg[i] += g[i][j]

    first = 0
    while first < n and not deg[first]:
        first += 1
    if first == n:
        print(-1)
        return

    v1, v2 = -1, -1
    bad = False
    for i in range(n):
        if deg[i] & 1:
            if v1 == -1:
                v1 = i
            elif v2 == -1:
                v2 = i
            else:
                bad = True

    if v1 != -1:
        g[v1][v2] += 1
        g[v2][v1] += 1

    st = []
    st.append(first)
    res = []
    while st:
        v = st[-1]
        for i in range(n):
            if g[v][i]:
                break
        if i == n:
            res.append(v)
            st.pop()
        else:
            g[v][i] -= 1
            g[i][v] -= 1
            st.append(i)

    if v1 != -1:
        for i in range(len(res) - 1):
            if (res[i] == v1 and res[i + 1] == v2) or (res[i] == v2 and res[i + 1] == v1):
                res = res[i + 1:] + res[1:i + 1]
                break

    bad = any(g[i][j] for i in range(n) for j in range(n))

    if bad:
        print(-1)
    else:
        for x in res:
            print(x, end=" ")

main()
