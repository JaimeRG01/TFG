# Probar la métrica que cuenta cuántos grafos computa bien

V = 8 # Vértices del grafo
A = (V * (V-1)) // 2 # Posibles aristas
N = (1 << A) # Posibles grafos
K = V // 2

import pickle 
import random


with open('clique.txt', 'rb') as handle: 
    data = handle.read() 
print("Cargando cliques")
s_cliques = pickle.loads(data) 
print("Cliques cargados")
print("Un total de: ", len(s_cliques))

# Funcion clique
def clique_fun() :
    f = [0] * N
    for i in s_cliques : f[i] = 1
    return f
print("Calculando la función de clique")
clique = clique_fun()

# Función que calcula la métrica
def mu(f) :
    ret = 0
    for i in range(N) :
        if f[i] == clique[i] : ret += 1
    return ret
# devuelve el m(f and g)
def combAND(f, g) :
    ret = 0
    for i in range(N) :
        if (f[i] & g[i]) == clique[i] : ret += 1
    return ret


'''
Por ahora para cadena almaceno su puntuación y también la puntuación desspués del AND



file = open("test_result.txt", "a")
test_cases = 10
for i in range(test_cases) :
    fun_bin1 = [random.randint(0, 1) for _ in range(N)]
    fun_bin2 = [random.randint(0, 1) for _ in range(N)]
    fun_and = [fun_bin1[j] & fun_bin2[j] for j in range(N)]
    print("aqui")
    s1 = mu(fun_bin1)
    s2 = mu(fun_bin2)
    s3 = mu(fun_and)
    file.write(str(s1) + " " + str(s2) + " " + str(s3) + "\n")
    file.write(str(s3-s1) + " " + str(s3-s2) + "\n")

file.close()
'''




# Crea una función cercana a la función objetivo
# Value es cuánto va a diferir la función de clique

def rand_values(value):
    difs = set()
    while len(difs) < value : 
        difs.add(random.randint(0, N-1))
    return difs


def compare_close_fun() :
    # 2^28 es lo máximo. Una forma de aproximarse es tomar porcentajes de ese valor. 
    # Con 50% ya hemos probado (es lo que sale con las funciones aleatorias)
    # Así que probamos desde ahí

    # Diferencias de puntuaciones con el objetivo
    values = [N-round(N*i/100) for i in range(85,100)]
    num_fun_to_test = 3
    # Cada una de estas tarda unos 6.5 minutos (en mi máquina)
    per = 85
    file = open("close_fun_result.txt", "a")
    for v in values :
        print("Probando con", per, "%") 
        for _ in range(num_fun_to_test) :
            print("\tIteración: ", _)
            print("\t\tGenerando valores donde diferir de clique")
            r1 = rand_values(v) # Para f1
            r2 = rand_values(v) # Para f2
            # Trabajamos con las funciones de forma ímplicitas (generarlas gasta mucha memoria)
            # La puntuación solo cambiará en los indices de r1 y r2
            mh = N
            r = r1.union(r2)
            print("\t\tComparando funciones")
            for i in r :
                if i in r1 : # Si cambia en f1
                    f1 = (clique[i] + 1) % 2
                else :
                    f1 = clique[i]
                if i in r2 : # Si cambia en f2
                    f2 = (clique[i] + 1) % 2
                else :
                    f2 = clique[i]
                if clique[i] != (f1 & f2) :
                    mh -= 1

            mf = N-v
            print(mf, mh)
            print("\t\tLa función ha crecido un total de: ", mh-mf)
            file.write(str(mf) + ", " + str(mh) + ", " + str(mh-mf) + "\n")
        per += 1
    file.close()

def compare_close_fun_dif_values() :
    values = [N-round(N*i/100) for i in range(85,100)]
    pers = [i for i in range(85, 100)] # Porcentajes
    num_of_tests = 40
    file = open("close_fun_dif_val_result.txt", "a")
    for it in range(num_of_tests) :
        print("Iteración número: ", it) 
        [p1,p2] = random.sample(pers,2)
        v1 = values[p1-85]
        v2 = values[p2-85]
        r1 = rand_values(v1) # Para f1
        r2 = rand_values(v2) # Para f2
        # Trabajamos con las funciones de forma ímplicitas (generarlas gasta mucha memoria)
        # La puntuación solo cambiará en los indices de r1 y r2
        mh = N
        r = r1.union(r2)
        print("\tComparando funciones")
        for i in r :
            if i in r1 : # Si cambia en f1
                f1 = (clique[i] + 1) % 2
            else :
                f1 = clique[i]
            if i in r2 : # Si cambia en f2
                f2 = (clique[i] + 1) % 2
            else :
                f2 = clique[i]
            if clique[i] != (f1 & f2) :
                mh -= 1
        mf1 = N-v1
        mf2 = N-v2
        print(mf1, mf2, mh)
        print("\tLa función ha crecido respecto a f1 un total de: ", mh-mf1)
        print("\tLa función ha crecido respecto a f2 un total de: ", mh-mf2)
        file.write(str(p1) + ", " + str(p2) + "\n")
        file.write(str(mf1) + ", " + str(mf2) + ", " + str(mh) + "\n")
    
    file.close()


#compare_close_fun()
compare_close_fun_dif_values()
print("FIN")