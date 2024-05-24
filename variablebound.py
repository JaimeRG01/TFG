
import sys
from scipy.special import binom
import matplotlib.pyplot as plt
sys.set_int_max_str_digits(0)

N = 100
K = N//2
A = (N * (N-1)) // 2
MAXT = N


# Encuentra v
def bin_search(n, k) :
    ini = 1
    fin = binom(n, k)
    result = fin
    b1 = binom(n, k)
    b2 = binom(k, 2) // 2
    while ini <= fin :
        mitad = (ini + fin) // 2
        b3 = binom(mitad, 2)
        b4 = binom(b3, b2)
        if b4 <= b1 :
            result = mitad
            ini = mitad + 1
        else :
            fin = mitad - 1
    return int(result)

# Encuentra v
def bin_search_with_not(n, k) :
    ini = 1
    fin = binom(n, k)
    result = fin
    b1 = binom(n, k)
    b2 = binom(k, 2) // 2
    while ini <= fin :
        mitad = (ini + fin) // 2
        b3 = 2*binom(mitad, 2)
        b4 = binom(b3, b2)
        if b4 <= b1*b1 :
            result = mitad
            ini = mitad + 1
        else :
            fin = mitad - 1
    return int(result)


x = []
y = []
xref = []
yref = []
for n in range(N) :
    k = n // 2
    v = bin_search_with_not(n, k)
    print("Para grafos de", n, "vertices se obtiene v =", v)
    x.append(n)
    y.append(v)
    xref.append(n)
    yref.append(n)


plt.plot(xref, yref, 'b-', label = "Vértices totales")
plt.plot(x,y, 'r-', label = 'Valores de $\mathcal{V}$')
plt.title("Evolución de $\mathcal{V}$")
plt.xlabel("Número de vértices $(n)$")
plt.ylabel("Número de vértices $(n)$")
plt.legend()
plt.show()








