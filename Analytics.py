import Parameters as P
import Variables as V
import Operators as O
import numpy as np
import matplotlib.pyplot as plt


def asigna_mvp():
    indice_mvp = np.argmax(V.array_energia_crom)
    if V.cromosoma_mvp[1] < V.array_energia_crom[indice_mvp]:
        V.cromosoma_mvp[0] = V.array_poblacion[indice_mvp]
        V.cromosoma_mvp[1] = V.array_energia_crom[indice_mvp]


def mayor_menor_promedio():
    for i in range(P.tam_poblacion):
        energia = O.calcula_energia_cromosoma(i)
        V.promedio += energia
        if energia > V.mayor:
            V.mayor = energia

        if energia < V.menor:
            V.menor = energia


def mostrar_grafica(grafica):
    plt.plot(grafica, V.array_maximos, 'r-', label='Maximo')
    plt.plot(grafica, V.array_minimos, 'b-', label='Minimo')
    plt.plot(grafica, V.array_promedios, 'g-', label='Promedio')
    plt.xlabel('Corridas')
    plt.ylabel('Distancia', multialignment='center')
    plt.legend()
    plt.show()
