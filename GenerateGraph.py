# Genera todos los grafos de 8 vértices con cliques de tamaño 4

V = 8 # Vértices del grafo
A = (V * (V-1)) // 2 # Posibles aristas
N = (1 << A) # Posibles grafos

# Por cada grafo calculamos si tiene un cliqué de tamaño V/2
K = V // 2

print(V, A, N, K)
# Usamos bits que va a ser más rápido que generar los subconjuntos recursivamente
# [0, N-1] codifica cada uno de los N posibles grafos -> Bit i a 1 es que tomamos la arista

bit_number = [[0 for _ in range(V)] for _ in range(V)] # Matriz que guarda el bit de cada arista 
adj_matrix = [[0 for _ in range(V)] for _ in range(V)] # Matriz que guarda el bit de cada arista 

count = 0
for v1 in range(V) :
    for v2 in range(v1 + 1, V):
        bit_number[v1][v2] = count
        count += 1

# Calculamos todos los subgrafos con K nodos (para comprobar si existe un cliqué de ese tamaño)

subgraphs = []

for mask in range(1, 1 << V) : # Posibles subgconjuntos de V elementos
    if mask.bit_count() == K:
        sg = []
        for bit in range(V) :
            if mask & (1 << bit) : sg.append(bit)
        assert len(sg) == K
        subgraphs.append(sg)

print("Subconjuntos de tamaño ", K, ":")
print(subgraphs)
print("\n")

ret = set()

for g in range(N) : # Por cada grafo
    # Comprobamos si tiene un cliqué de tamaño K recorriendo subgraphs
    clique = False
    for sg in subgraphs :
        aux = True
        for i in range(K) :
            for j in range(i+1, K) :
                if g & (1 << bit_number[sg[i]][sg[j]]) == 0 : 
                    aux = False
                    break
            if not aux: break # Si el subconjunto actual no es válido
        if aux: 
            clique = True
            break # Si el subconjunto actual es válido
    if clique : # g tiene un clique de tamaño K
        ret.add(g)
        # Crear el grafo para verlo basicamente

        graph = [list() for _ in range(V)]
        v1 = 0
        v2 = 1
        for bit in range(A) : 
            #print("bit: ", bit, "bin: ", 1 << bit)
            if g & (1 << bit): # Si bit está activo
                graph[v1].append(v2)
                graph[v2].append(v1)
            v2 += 1
            if v2 == V :
                v1 += 1
                v2 = v1 + 1
        


# Para serializar
import pickle 

with open('clique.txt', 'rb') as handle: 
    data = handle.read() 

d = pickle.loads(data) 


