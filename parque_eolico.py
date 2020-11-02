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

    P.chances_mutacion = (C.const_mutacion / P.corridas) * (cor + 1) + C.mutacion_inicial
    P.chances_crossover = -(C.const_crossover / P.corridas) * (cor + 1) + C.crossover_inicial

    O.calcula_energia_poblacion()
    O.fitness()
    if resp == 's' or resp == 'S':
        V.array_elite = O.elite()
    O.crossover()
    O.mutacion()
    V.array_poblacion = O.ruleta()
    if resp == 's' or resp == 'S':
        for eli in range(len(V.array_elite)):
            V.array_poblacion.append(V.array_elite[eli])

    O.calcula_energia_poblacion()

    #A.mayor_menor_promedio(cor)

    A.asigna_mvp(cor)

    #V.array_poblacion = np.random.permutation(V.array_poblacion).tolist()

"""for f in range(P.filas):
    print(V.cromosoma_mvp[0][f])

for f in range(P.filas):
    print(V.cromosoma_mvp[2][f])

print(round(V.cromosoma_mvp[1], 2))

print(V.cromosoma_mvp[3])"""

#A.mostrar_grafica(grafica)

A.mostrar_grilla()

print()
