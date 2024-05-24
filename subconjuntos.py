from hungarian import matching
import random 
from math import sqrt
from random import sample
import matplotlib.pyplot as plt
from collections import deque

N = 8 # Vértices
K = 4 # Tamaño del clique
A = N * (N-1) // 2
subsets = []


def generate_subset(n, ini, sz, acc) : 
    if sz == 0: 
        subsets.append(acc.copy())
    elif ini <= n: 
        acc.append(ini)
        generate_subset(n, ini+1, sz-1, acc)
        acc.pop()
        generate_subset(n, ini+1, sz, acc)

# Genera la función booleana que computa el clique
def generate_fun_clique(subsets) :
    res = []
    idx = [[0 for i in range(N+1)] for j in range(N+1)]
    cnt = 1
    for i in range(1,N+1) :
        for j in range(i+1, N+1) :
            idx[i][j] = cnt
            cnt += 1
    for s in subsets : 
        f = []
        for i in range(K) :
            for j in range(i+1, K) :
                f.append(idx[s[i]][s[j]])
        res.append(f)
    return res

# Calcula cuántos literales de f están en g
def common_literals(f, g) :
    res = 0
    for i in f :
        if i in g: res += 1
    return res

# Calcula la métrica. Usa el algoritmo húngaro para asignar el máximo posible
def m(f) :
    n = len(f)
    m = len(clique)
    # Costes negativos para maximizar
    # min (f(x)) = -max(-f(x))
    if n <= m : 
        mat = [[-common_literals(f[i], clique[j]) for j in range(m)] for i in range(n)]
    else : 
        mat = [[-common_literals(f[i], clique[j]) for i in range(n)] for j in range(m)]
    #for i in mat : print(i)
    #print(n, m)
    res = -matching(mat)
    return res

# Comprueba si f es prefijo de g
def is_prefix(f, g) :
    if len(f) > len(g) : return False
    else : return f == g[:len(f)]

# Reduce f. CUIDADO CON LOS NOT
def reduce(f, k = (K * (K-1) // 2)) :
    l = len(f)
    for i in range(l) :
        f[i] = list(set(f[i]))
        f[i].sort()
    f.sort()
    # Quitar elementos que no aportan informacion
    res = []
    mark = [False] * l
    # Marcamos las que son demasiado largas

    '''ESTE FOR SOLO CUANDO NO HAY NOTS'''
    # for i in range(l) :
        # if len(f[i]) > k : mark[i] = True
    for i in range(l) :
        if mark[i] : continue
        for j in range(i+1, l) :
            if is_prefix(f[i], f[j]) : mark[j] = True
        res.append(f[i])
    return res  

# Calcula f and g
# Junta todos los pares de f y g 
def combAND(f, g, k = (K * (K-1) // 2)) :
    aux = []
    n1 = len(f); n2 = len(g)
    for i in range(n1) :
        for j in range(n2) :
            aux.append(f[i] + g[j])

    return reduce(aux)

# Función aleatoria
def get_rand_fun() :
    l = random.randint(1, len(clique))
    aux = sample(clique, l)
    res = []
    for i in aux : 
        l = random.randint(1, len(i))
        res.append(sample(i, l))
    return res

# Función aleatoria de baja puntuación
def get_rand_low_fun(punt) : 
    aux = sample(clique, punt)
    res = []
    for i in aux : 
        r = min(len(i), punt)
        res.append(sample(i, r))
        punt -= r
        if punt == 0: break
    return res

# Función aleatoria con NOT
def get_rand_fun_with_not() :
    l = random.randint(1, len(clique))
    aux = sample(clique, l)
    res = []
    for i in aux : 
        l = random.randint(1, len(i))
        res.append(sample(i, l))

    for i in range(len(res)) :
        l = random.randint(0, len(res[i]))
        neg = sample(range(0, len(res[i])), l)
        for j in neg : res[i][j] *= -1
    return res

# AND con NOT
def combAND_with_not(f, g) :
    aux = []
    n1 = len(f); n2 = len(g)
    for i in range(n1) :
        for j in range(n2) :
            aux.append(f[i] + g[j])

    # Eliminar aquellas que se cancelan por los not
    ret = []
    for i in aux :
        ok = True
        for j in i :
            if (-j) in i : 
                ok = False
                break
        if ok : ret.append(i)
    return reduce(ret)

# Compara funciones aleatorias
def compare_rand_fun() :
    iter = 100
    fig = plt.figure(figsize = (8,5))
    x = []
    y = []
    for _ in range(iter) :
        print("Iteración número:", _+1)
        f = reduce(get_rand_fun())
        g = reduce(get_rand_fun())
        h = combAND(f, g)
        m1 = m(f)
        m2 = m(g)
        m3 = m(h)
        #print(m1, m2, " -> ", m3)
        x.append(m1); y.append(m3)
        x.append(m2); y.append(m3)
   
    plt.plot(x, y, 'ro', label = '$\mu_x(f \wedge g)$')
    plt.xlabel('$\mu_x$ antes de AND')
    plt.ylabel('$\mu_x$ despues de AND')
    title = "Comparación de " + str(iter) + " pares de funciones aleatorias"
    plt.title(title)
    plt.legend()
    plt.show()

# Compara funciones aleatorias con NOT
def compare_rand_fun_with_not() :
    iter = 10000
    fig = plt.figure(figsize = (8,5))
    x = []
    y = []
    maxi_rand = -1
    maxi_and = -1
    for _ in range(iter) :
        print("Iteración número:", _+1)
        f = reduce(get_rand_fun_with_not())
        g = reduce(get_rand_fun_with_not())
        h = combAND_with_not(f, g)
        m1 = m(f)
        m2 = m(g)
        m3 = m(h)
        maxi_rand = max(m1, m2, maxi_rand)
        maxi_and = max(maxi_and, m3)
        #print(m1, m2, " -> ", m3)
        x.append(m1); y.append(m3)
        x.append(m2); y.append(m3)
    
    plt.plot(x, y, 'ro', label = '$\mu_x(f \wedge g)$')
    plt.xlabel('$\mu_x$ antes de AND')
    plt.ylabel('$\mu_x$ despues de AND')
    title = "Comparación de " + str(iter) + " pares de funciones aleatorias con NOT"
    plt.title(title)
    plt.legend()
    plt.show()

# Genera una función con m cláusulas donde cada cláusula tiene 
# n variables y en total usa el mínimo número de variables posibles
def endogamic_fun(n, m, reverse = False) :
    S = [i for i in range(1, A+1)]
    if reverse : S.reverse()
    #random.shuffle(S)
    res = []
    q = deque()
    ini = [S[i] for i in range(n)]
    ini.sort()
    vis = set()
    vis.add(tuple(ini))
    res.append(ini)
    q.append((ini, n))
    cnt = 1
    while cnt < m and len(q) > 0 : 
        (cur, id) = q.popleft()
        i = 0
        if id >= len(S) : break
        while i < len(cur) and cnt < m :
            new = cur.copy()
            new[i] = S[id]
            new.sort()
            if not tuple(new) in vis :
                vis.add(tuple(new))
                res.append(new.copy())
                q.append((new.copy(), id+1))
                cnt += 1
            i += 1
    res.sort()
    return res

# OR de dos funciones
def combOR(f, g) :
    res = f + g
    return reduce(res)

# Simula el circuito
def simulate_circuit() :
    # Variables
    S = [([[i]],1) for i in range(1, A+1)]
    
    or_iter = 10
    and_iter = 10
    max_size = len(clique)
    limit = 300
    iter = 100
    xOR = []; xAND = []
    yOR = []; yAND = []
    for _ in range(iter) :
        for i in range(or_iter) :
            (f, aux) = random.choice(S)
            (g, aux) = random.choice(S)
            h = combOR(f, g)
            if len(h) <= max_size and h != []: 
                m1 = m(f); m2 = m(g); m3 = m(h)
                if m3 == 0 : print(f, g)
                xOR.append(m1); xOR.append(m2)
                yOR.append(m3); yOR.append(m3)
                S.append((h, m3))
        for i in range(and_iter) :
            (f, aux) = random.choice(S)
            (g, aux) = random.choice(S)
            h = combAND(f, g)
            if len(h) <= max_size and h != []: 
                m1 = m(f); m2 = m(g); m3 = m(h)
                xAND.append(m1); xAND.append(m2)
                yAND.append(m3); yAND.append(m3)
                S.append((h, m3))
        
        print("Iteración: ", _+1)
        S.sort(key = lambda elem : elem[1], reverse = True)
        while len(S) > limit : S.pop()
    
    
    fig = plt.figure(figsize = (8,5))
    #plt.xlim([0,420])
    plt.plot(xAND, yAND, 'ro')
    plt.plot(xOR, yOR, 'bo')
    plt.show()

# Simula el circuito con NOT
def simulate_circuit_with_not() :
    # Variables
    S1 = [([[i]],1) for i in range(1, A+1)]
    S2 = [([[-i]],0) for i in range(1, A+1)]
    S = S1 + S2
    or_iter = 15
    and_iter = 15
    max_size = 150
    limit = 300
    iter = 300
    xOR = []; xAND = []
    yOR = []; yAND = []
    for _ in range(iter) :
        for i in range(or_iter) :
            (f, aux) = random.choice(S)
            (g, aux) = random.choice(S)
            h = combOR(f, g)
            if len(h) <= max_size and h != []: 
                m1 = m(f); m2 = m(g); m3 = m(h)
                # if m3 == 0 : print(f, g)
                xOR.append(m1); xOR.append(m2)
                yOR.append(m3); yOR.append(m3)
                S.append((h, m3))
        for i in range(and_iter) :
            (f, aux) = random.choice(S)
            (g, aux) = random.choice(S)
            h = combAND_with_not(f, g)
            if len(h) <= max_size and h != []: 
                m1 = m(f); m2 = m(g); m3 = m(h)
                xAND.append(m1); xAND.append(m2)
                yAND.append(m3); yAND.append(m3)
                S.append((h, m3))
        
        print("Iteración: ", _+1)
        S.sort(key = lambda elem : elem[1], reverse = True)
        while len(S) > limit : S.pop()
    
    
    
    print("Incremento máximo:", S[0][1])
    fig = plt.figure(figsize = (8,5))
    #plt.xlim([0,420])
    plt.plot(xAND, yAND, 'ro', alpha = 0.5, label = "Incremento con AND")
    plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Simulación tras " + str(iter) + " iteraciones"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("$\mu_x(f)$")
    plt.show()
    
# Compara funciones endogámicas de poca puntuación
def compare_low_end_fun() :

    M = len(clique)
    tam = 100
    tope = int(sqrt(M))
    end_funs1 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope)) for _ in range(tam)]
    end_funs2 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope), True) for _ in range(tam)]
    #for f in end_funs1 : print(f)
    #for f in end_funs2 : print(f)


    x = []
    y = []

    mf1 = [m(f) for f in end_funs1]
    mf2 = [m(f) for f in end_funs2]
    maxpunt = {}
    for i in range(len(end_funs1)):
        maxpunt[mf1[i]] = 0 
        maxpunt[mf2[i]] = 0

    maxi = -1
    for i in range(tam) :
        print("Iteración:", i)
        for j in range(tam) :
            h = combAND(end_funs1[i], end_funs2[j])
            m3 = m(h)
            x.append(mf1[i]); y.append(m3)
            x.append(mf2[j]); y.append(m3)
            maxi = max(maxi, mf1[i], mf2[j])
            maxpunt[mf1[i]] = max(maxpunt[mf1[i]], m3)
            maxpunt[mf2[j]] = max(maxpunt[mf2[j]], m3)

    plt.plot(x, y, 'ro', label = "$\mu_x(f_{s,t})$")
    vals = [(a,b) for a,b in maxpunt.items()]
    vals.sort(key = lambda x : x[0])
    v1 = [i[0] for i in vals]
    v2 = [i[1] for i in vals]
    plt.plot(v1, v2, '-', color = 'orange', label = "Incremento máximo")

    x = []
    y = []
    rand_low_funs = []
    m_rand_low_funs = []
    iter = 50
    print("Maximo:", maxi)
    for j in range(1, maxi+1) :
        for i in range(iter) :    
            f = reduce(get_rand_low_fun(j))
            mf = m(f)
            rand_low_funs.append(f)
            m_rand_low_funs.append(mf)

    for i in range(len(rand_low_funs)) :
        print(i)
        for j in range(i+1, len(rand_low_funs)) :

            h = combAND(rand_low_funs[i], rand_low_funs[j])
            m3 = m(h)
            m1 = m_rand_low_funs[i]
            m2 = m_rand_low_funs[j]
            x.append(m1); y.append(m3)
            x.append(m2); y.append(m3)

    plt.plot(x, y, 'bo', label = "$\mu_x(f)$")
    plt.legend()
    plt.xlabel("$\mu_x$ antes de AND")
    plt.ylabel("$\mu_x$ después de AND")
    plt.title("$f_{s,t}$ vs $f$")
    plt.show()

# Compara funciones endogámicas de más puntuación
def compare_big_end_fun() : 
    
    M = len(clique)
    tam = 10
    tope = M // 2
    end_funs1 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope)) for _ in range(tam)]
    end_funs2 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope), True) for _ in range(tam)]
    #for f in end_funs1 : print(f)
    #for f in end_funs2 : print(f)


    x = []
    y = []

    mf1 = [m(f) for f in end_funs1]
    mf2 = [m(f) for f in end_funs2]
    maxpunt = {}
    for i in range(len(end_funs1)):
        maxpunt[mf1[i]] = 0 
        maxpunt[mf2[i]] = 0

    maxi = -1
    for i in range(tam) :
        print("Iteración:", i)
        for j in range(tam) :
            h = combAND(end_funs1[i], end_funs2[j])
            m3 = m(h)
            x.append(mf1[i]); y.append(m3)
            x.append(mf2[j]); y.append(m3)
            maxi = max(maxi, mf1[i], mf2[j])
            maxpunt[mf1[i]] = max(maxpunt[mf1[i]], m3)
            maxpunt[mf2[j]] = max(maxpunt[mf2[j]], m3)

    plt.plot(x, y, 'ro', label = "$\mu_x(f_{s,t})$", zorder = 4)
    vals = [(a,b) for a,b in maxpunt.items()]
    vals.sort(key = lambda x : x[0])
    v1 = [i[0] for i in vals]
    v2 = [i[1] for i in vals]
    plt.plot(v1, v2, '-', color = 'orange', label = "Incremento máximo", zorder = 6)

    x = []
    y = []
    rand_low_funs = []
    m_rand_low_funs = []
    iter = 50
    print("Maximo:", maxi)
    for i in range(iter) :    
        f = reduce(get_rand_low_fun(random.randint(1,maxi)))
        mf = m(f)
        rand_low_funs.append(f)
        m_rand_low_funs.append(mf)

    for i in range(len(rand_low_funs)) :
        print(i)
        for j in range(i+1, len(rand_low_funs)) :

            h = combAND(rand_low_funs[i], rand_low_funs[j])
            m3 = m(h)
            m1 = m_rand_low_funs[i]
            m2 = m_rand_low_funs[j]
            x.append(m1); y.append(m3)
            x.append(m2); y.append(m3)

    plt.plot(x, y, 'bo', label = "$\mu_x(f)$", zorder = 8)
    plt.legend()
    plt.xlabel("$\mu_x$ antes de AND")
    plt.ylabel("$\mu_x$ después de AND")
    plt.title("$f_{s,t}$ vs $f$")
    plt.show()





generate_subset(N, 1, K, [])
# prin(subsets)
clique = generate_fun_clique(subsets)
# print(clique)
print("Valor función objetivo: ", m(clique))


'''LLAMAR A LO QUE SE NECESITE'''


#simulate_circuit_with_not()

#compare_rand_fun_with_not()

#compare_rand_fun()

#compare_low_end_fun()