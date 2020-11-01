import Parameters as P
import Variables as V
import Operators as O
import numpy as np
import matplotlib.pyplot as plt


def asigna_mvp(cor):
    indice_mvp = np.argmax(V.array_fitness)
    if V.cromosoma_mvp[1] <= np.sum(V.array_energia_molino[indice_mvp]):
        V.cromosoma_mvp[0] = V.array_poblacion[indice_mvp]
        V.cromosoma_mvp[1] = np.sum(V.array_energia_molino[indice_mvp])
        V.cromosoma_mvp[2] = V.array_energia_molino[indice_mvp]
        V.cromosoma_mvp[3] = indice_mvp
        V.cromosoma_mvp[4] = cor


def mayor_menor_promedio(cor):
    for i in range(P.tam_poblacion):
        energia = np.sum(V.array_energia_molino[i])
        V.promedio += energia
        if energia > V.mayor:
            V.mayor = energia

        if energia < V.menor:
            V.menor = energia

    V.array_maximos[cor] = V.mayor
    V.array_minimos[cor] = V.menor
    V.array_promedios[cor] = V.promedio / P.tam_poblacion


def mostrar_grafica(grafica):
    plt.plot(grafica, V.array_maximos, 'r-', label='Maximo')
    plt.plot(grafica, V.array_minimos, 'b-', label='Minimo')
    plt.plot(grafica, V.array_promedios, 'g-', label='Promedio')
    plt.xlabel('Corridas')
    plt.ylabel('Distancia', multialignment='center')
    plt.legend()
    plt.show()
