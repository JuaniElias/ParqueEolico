import numpy as np
import random

tam_poblacion = 2
rugosidad = 0.0024
chances_crossover = 2
chances_mutacion = 0.20
filas = 10
col = 10
cte_long_estela = 12            #podemos jugar con este valor
cant_molinos = 25
viento_puro = 20
viento = [0] * 10


array_fitness = [0] * tam_poblacion             #se guardan los totales de energia de todos los cromosomas
array_poblacion = [0] * tam_poblacion           #se guardan todos los cromosomas
array_energia_molino = [0] * tam_poblacion      #se guarda la energia producida por cada molino


class Molino:
    def __init__(self, modelo, altura, diametro, velocidad_potencia):
        self.modelo = modelo
        self.altura = altura
        self.diametro = diametro
        self.velocidad_potencia = velocidad_potencia
        self.distancia_minima = 2 * diametro
        self.arrastre = 1 / (2 * np.log(altura / rugosidad))
        self.induccion_axial = 1 / 3
        self.radio_estela = 2 * diametro  # diametro/2 * 4 (valor maximo de gama), preguntar


class Viento:
    def __init__(self, velocidad, potencia):
        self.velocidad = velocidad
        self.potencia = potencia


molinos = Molino("GAMESA G47", 55, 47, 660)

viento[0] = Viento(4, 0)
viento[1] = Viento(5, 53)
viento[2] = Viento(6, 106)
viento[3] = Viento(7, 166)
viento[4] = Viento(8, 252)
viento[5] = Viento(9, 350)
viento[6] = Viento(10, 464)
viento[7] = Viento(11, 560)
viento[8] = Viento(12, 630)
viento[9] = Viento(25, 660)

molinos = Molino("GAMESA G47", 55, 47, viento)


def ruleta():
    base = 0
    cant_casilleros = 0

    for i in range(0, tam_poblacion):
        casilleros = round(array_fitness[i] * 100)
        cant_casilleros = cant_casilleros + casilleros
    roulette = [0] * cant_casilleros

    for i in range(0, tam_poblacion):
        casilleros = round(array_fitness[i] * 100)

        for j in range(base, base + casilleros):
            roulette[j] = i
        base = base + casilleros

    bolilla = random.randint(0, cant_casilleros - 1)
    return roulette[bolilla]


def retorna_energia(velocidad):
    velocidad = round(velocidad)
    for i in range(0, 10):
        if velocidad == molinos.velocidad_potencia[i].velocidad:
            return molinos.velocidad_potencia[i].potencia
            break
    if 13 <= velocidad <= 25:
        return molinos.velocidad_potencia[9].potencia
    elif velocidad > 25 or 0 <= velocidad < 4:
        return molinos.velocidad_potencia[0].potencia


def calcula_velocidad_viento(velocidad_inicial, x):
    velocidad_final = velocidad_inicial * (1 - (2 * molinos.induccion_axial) / np.square(
        1 + (molinos.arrastre * (molinos.distancia_minima * x) / molinos.radio_estela)))
    return velocidad_final


def fitness(k):                     #pensar para 3 molinos consecutivos
    viento_actual = viento_puro
    energia = 0
    m_energia = np.zeros((10, 10))
    m = array_poblacion[k]
    #def matriz de vientos que me arme un 10x10 con todos los valores del viento
    for i in range(0, filas):
        flag = True
        cont = 0
        for j in range(0, col):
            if m[i][j] == 1:
                if flag or cte_long_estela * molinos.diametro < cont * molinos.distancia_minima:    # entra si el viento es puro
                    flag = False
                    energia = energia + retorna_energia(viento_puro)
                    m_energia[i][j] = retorna_energia(viento_puro)
                else:                                                                               # entra si el viento es turbulento
                        velocidad_final = calcula_velocidad_viento(viento_puro, cont)
                        energia = energia + retorna_energia(velocidad_final)
                        m_energia[i][j] = retorna_energia(velocidad_final)
                cont = 1

            else:
                if cont != 0:
                    cont += 1
    array_energia_molino[k] = m_energia
    array_fitness[k] = energia


def poblacion_inicial():
    for k in range(0, tam_poblacion):
        m = np.zeros((10, 10))
        cont = 0
        while cont < 25:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if m[x][y] == 0:
                m[x][y] = 1
                cont = cont + 1
        array_poblacion[k] = m


def crossover():
    for i in range(0, tam_poblacion, 2):
        cros = random.random()

        if cros < chances_crossover:

                                                # CROSSOVER POR COLUMNAS
            hijo1_molinos = np.concatenate((array_poblacion[i], array_poblacion[i+1]), axis=1)       #matriz 20x10 molinos
            hijo1_potencia = np.concatenate((array_energia_molino[i], array_energia_molino[i+1]), axis=1)          #matriz 20x10 potencia
            sumatoria_h1 = hijo1_potencia.sum(axis=0)        #devuelve un arreglo con la sumatoria de todas las columnas
            permutacion = np.argsort(-sumatoria_h1)

            hijo1 = np.zeros((10, 10))
            for columna in range(0, 10):
                for fila in range(0, 10):
                    hijo1[fila][columna] = hijo1_molinos[fila][permutacion[columna]]


                                                #CROSSOVER POR FILAS
            hijo2_molinos = np.concatenate((array_poblacion[i], array_poblacion[i + 1]), axis=0)    # matriz 10x20 molinos
            hijo2_potencia = np.concatenate((array_energia_molino[i], array_energia_molino[i + 1]), axis=0)  # matriz 10x20 potencia
            sumatoria_h2 = hijo2_potencia.sum(axis=1)  # devuelve un arreglo con la sumatoria de todas las filas
            permutacion = np.argsort(-sumatoria_h2)

            hijo2 = np.zeros((10, 10))
            for fila in range(0, 10):
                for columna in range(0, 10):
                    hijo2[fila][columna] = hijo2_molinos[permutacion[fila]][columna]




poblacion_inicial()
for i in range(0, tam_poblacion):
    fitness(i)
crossover()
for i in range(0, tam_poblacion):
    #print(array_poblacion[i])
    print(array_fitness[i])



