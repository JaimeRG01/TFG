
import matplotlib.pyplot as plt

# Para comparar el fichero close_fun_result.txt, que tiene guardados los datos
# de las comparaciones entre funciones con el mismo porcentaje de puntuación
def compare_close_fun_eq() :
    file = open("close_fun_result.txt", "r")
    results = dict()
    difs = dict()
    per = 85
    cont = 0
    for line in file:
        aux = line.split(', ')
        if not per in results : 
            results[per] = int(aux[1])
            difs[per] = int(aux[2])
        else : 
            results[per] = max(results[per], int(aux[1]))
            difs[per] = max(difs[per], int(aux[2]))
        cont += 1
        if cont == 3 : 
            per += 1
            cont = 0

    file.close()

    for key, val in difs.items() : 
        print(key, "&", val)

    x = []
    y = []
    N = (1<<28)
    for i in range(85,100) :
        x.append(i)
        y.append((N-results[i])/difs[i])
    plt.plot([50,x[0]], [21, y[0]], 'o-', color = 'red', label = "Descenso desde $f_{50}$", zorder = 10)
    plt.plot(x, y, 'b-', label = "Niveles esperados")
    #plt.plot(x, y, 'b-', label = "Niveles esperados")
    plt.plot(100, 0, 'o', color = 'purple', markersize = 7, label = "Objetivo", zorder = 4)
    plt.plot([x[-1],100], [y[-1], 0], '-', color = 'orange', label = "Salto detectado", zorder = 2)
    plt.xlabel("Porcentaje $p$ (%)")
    plt.ylabel("Mínimo número de puertas para $f_p$")
    plt.title("Evolución tras comparar funciones $f_p$ del mismo tipo")
    plt.legend()
    plt.show()

# Para comparar el fichero close_fun_dif_val_result.txt, que tiene guardados los datos
# de las comparaciones entre funciones con distinto porcentaje de puntuación
def compare_close_fun_dif() :
    file = open("close_fun_dif_val_result.txt", "r")
    lines = [l for l in file]    
    file.close()
 
    # Formato : Cada caso son dos líneas de la forma
    # porcentaje1, porcentaje2
    # mu(f1), mu(f2), mu(f1 and f2)
    funs1 = [] # funciones f1 -> [[porcentaje, mu(f)]]
    funs2 = [] # funciones f2 -> [[porcentaje, mu(f)]]
    funs_and = [] # [mu(f1[i] and f2[i])]
    for i in range(0, len(lines), 2) :
        p1, p2     = [int(j) for j in lines[i].split(', ')]
        m1, m2, m3 = [int(j) for j in lines[i+1].split(', ')]
        funs1.append([p1, m1])
        funs2.append([p2, m2])
        funs_and.append(m3)
    
    n = len(funs1)
    x = []; y = []
    for i in range(n) :
        x.append(funs1[i][0])
        x.append(funs2[i][0])
        y.append(funs_and[i])
        y.append(funs_and[i])

    N = 1<<28 
    maxpt = [0 for i in range(85, 100)]
    minpt = [N for i in range(85, 100)]
    midpt = [0 for i in range(85, 100)]
    absc = [i for i in range(85, 100)]
    # Máximo, mínimo e inicial crecimiento para un porcentaje
    for i in range(n) :
        p1 = funs1[i][0]-85
        p2 = funs2[i][0]-85
        m = funs_and[i]
        maxpt[p1] = max(maxpt[p1], m)
        minpt[p1] = min(minpt[p1], m)
        
        maxpt[p2] = max(maxpt[p2], m)
        minpt[p2] = min(minpt[p2], m)

        # Puntuación incial
        midpt[p1] = funs1[i][1]
        midpt[p2] = funs2[i][1]
    


    plt.title("Evolución de funciones $f_p$ de distinto tipo")
    plt.plot(x, y, 'ro', label = "$\mu_s(f_{p_1} \wedge f_{p_2})$")
    plt.plot(absc, minpt, '-', label = "Valores mínimos de $\mu_s$")
    plt.plot(absc, maxpt, '-', label = "Valores máximos de $\mu_s$")
    plt.plot(absc, midpt, 'o-', label = "Valores iniciales")
    plt.plot(100, N, 'o', color = "purple", markersize = 7, label = "$\mu_s(f_{clique})$")
    plt.xlabel("Porcentaje (%)")
    plt.ylabel("$\mu_s(f)$")
    plt.legend()
    plt.show()




# LLamar en función de lo que se quiera

compare_close_fun_eq()
# compare_close_fun_dif()
