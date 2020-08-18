import numpy as np
import random


m_energia = np.zeros((10, 10))
tam_poblacion = 2
array_fitness = [0] * tam_poblacion
rugosidad = 0.0024
chances_crossover = 0.75
chances_mutacion = 0.20
filas = 10
col = 10
cte_long_estela = 18
cant_molinos = 25
array_poblacion = [0] * tam_poblacion
velocidad_viento = 20
viento = [0] * 10
energia_total = 0


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


def calcula_velocidad_viento(velocidad_inicial):
    velocidad_final = velocidad_inicial * (1 - (2 * molinos.induccion_axial) / np.square(
        1 + (molinos.arrastre * molinos.distancia_minima / molinos.radio_estela)))
    return velocidad_final


def fitness(energia):
    for i in range(0, filas):
        flag = True
        cont = 0
        for j in range(0, col):
            if m[i][j] == 1:
                if flag or cte_long_estela * molinos.diametro < cont * molinos.distancia_minima:  # u0
                    flag = False
                    energia = energia + retorna_energia(velocidad_viento)
                else:  # ux
                    velocidad_final = calcula_velocidad_viento(velocidad_viento)
                    energia = energia + retorna_energia(velocidad_final)
                cont = 1
            else:
                if cont != 0:
                    cont += 1


def poblacion_inicial():
    for k in range(0, tam_poblacion):
        m = np.zeros((10, 10))
        cont = 0
        while cont < cant_molinos:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if m[x][y] == 0:
                m[x][y] = 1
                cont = cont + 1
        array_poblacion[k] = m


"""def crossover():
    for i in range(0, tam_poblacion, 2):
        cros = random.random()

        if cros < chances_crossover:"""

poblacion_inicial()
for i in range(0, tam_poblacion):
    print(array_poblacion[i])


