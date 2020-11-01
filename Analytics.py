import Parameters as P
import Variables as V
import Operators as O
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


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
    plt.ylabel('Energia', multialignment='center')
    plt.legend()
    plt.show()


def mostrar_grilla():
    colormap = colors.ListedColormap(["#90E577", "grey"])
    im = plt.imread('images/arrow_wind.png')

    f, axarr = plt.subplots(1, 2)

    axarr[0].axis("off")
    axarr[0].imshow(im)
    axarr[1].grid(which='minor', color='black', linestyle='-', linewidth=2)
    axarr[1].imshow(V.cromosoma_mvp[0], cmap=colormap)

    titulo = str(round(V.cromosoma_mvp[1], 2))

    plt.title("Esta distribución de molinos produce " + titulo + " kW de energía", size=18)
    plt.grid(b=True, color='#666666', linestyle='-')

    axarr[1].set_xticks(np.arange(-.5, 10, 1))
    axarr[1].set_yticks(np.arange(-.5, 10, 1))

    axarr[1].set_xticklabels(np.arange(0, 11, 1))
    axarr[1].set_yticklabels(np.arange(0, 11, 1))

    axarr[1].xaxis.tick_top()

    plt.show()
