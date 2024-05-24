# Algoritmo húngaro

def matching(mat) :
    if len(mat) == 0 : return 0
    n = len(mat) + 1
    m = len(mat[0]) + 1
    p = [0] * m
    u = [0] * n
    v = [0] * m
    inf = 1000000
    for i in range(1, n) :
        p[0] = i
        j0 = 0
        dist = [inf] * m
        pre = [-1] * m
        done = [False] * (m+1)
        while True : # Dijkstra
            done[j0] = True
            i0 = p[j0]; j1 = 0
            delta = inf
            for j in range(1, m) :
                if not done[j] :
                    cur = mat[i0-1][j-1] - u[i0] - v[j]
                    if cur < dist[j] : 
                        dist[j] = cur
                        pre[j] = j0
                    if dist[j] < delta : 
                        delta = dist[j]
                        j1 = j
            for j in range(m) :
                if done[j] :
                    u[p[j]] += delta
                    v[j] -= delta
                else : dist[j] -= delta
            j0 = j1
            if not p[j0] : break
        while j0 : 
            j1 = pre[j0]
            p[j0] = p[j1]
            j0 = j1
    return -v[0]