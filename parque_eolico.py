import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors

import Models as M
import Parameters as P
import Operators as O
import Analytics as A
import Variables as V
import Constants as C

# resp = input('Quiere hacer elitismo (s/n): ')

resp = 's'
grafica = np.linspace(0, P.corridas, P.corridas)

O.poblacion_inicial()
V.cromosoma_mvp[1] = 0
for cor in range(P.corridas):

    V.mayor = 0
    V.menor = 40000
    V.promedio = 0

    if cor != 0:
        P.chances_mutacion = P.chances_mutacion ** cor

    for k in range(P.tam_poblacion):
        V.array_energia_crom[k] = O.calcula_energia_cromosoma(k)
    O.fitness()
    if resp == 's' or resp == 'S':
        V.array_elite = O.elite()
    O.crossover()
    O.mutacion()
    V.array_poblacion = O.ruleta()
    if resp == 's' or resp == 'S':
        for eli in range(len(V.array_elite)):
            V.array_poblacion.append(V.array_elite[eli])

    V.array_poblacion = np.random.permutation(V.array_poblacion).tolist()

    A.asigna_mvp()
    A.mayor_menor_promedio()

    V.array_maximos[cor] = V.mayor
    V.array_minimos[cor] = V.menor
    V.array_promedios[cor] = V.promedio / P.tam_poblacion

for f in range(P.filas):
    print(V.cromosoma_mvp[0][f])

for k in range(P.tam_poblacion):
    V.array_energia_crom[k] = O.calcula_energia_cromosoma(k)
O.fitness()

print(V.cromosoma_mvp[1])


A.mostrar_grafica(grafica)

colormap = colors.ListedColormap(["#90E577", "grey"])
plt.figure(figsize=(5, 5))
plt.imshow(V.cromosoma_mvp[0], cmap=colormap)
plt.axis('off')
plt.show()

