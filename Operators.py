import Parameters as P
import Constants as C
import Variables as V
import numpy as np
import random


def poblacion_inicial():
    for i in range(P.tam_poblacion):
        m = np.zeros((P.filas, P.columnas), dtype=int)
        cont = 0
        while cont < 25:
            x = random.randint(0, P.filas - 1)
            y = random.randint(0, P.columnas - 1)
            if m[x][y] == 0:
                m[x][y] = 1
                cont = cont + 1
        V.array_poblacion[i] = m


def crossover():
    cros_corridas = len(V.array_poblacion)
    for i in range(0, cros_corridas, 2):
        cros = random.random()

        if cros < P.chances_crossover:
            #                               -- CROSSOVER POR COLUMNAS (Hijo 1)--
            # Matriz 20x10 molinos
            padres_concat_columnas = np.concatenate((V.array_poblacion[i], V.array_poblacion[i + 1]), axis=1)
            # Matriz 20x10 potencia
            hijo1_potencia = np.concatenate((V.array_energia_molino[i], V.array_energia_molino[i + 1]), axis=1)

            sumatoria_h1 = hijo1_potencia.sum(axis=0)  # Devuelve un arreglo con la sumatoria de todas las columnas
            permutacion = np.argsort(-sumatoria_h1)

            # Reordena las columnas segun la sumaoria de potencias (sumatoria_h1)
            hijo1_concat_columnas = padres_concat_columnas[:, permutacion]
            # Elimina las columnas sobrantes
            hijo1 = hijo1_concat_columnas[:, :P.columnas]

            #                                 -- CROSSOVER POR FILAS (Hijo 2)--
            # Matriz 10x20 molinos
            padres_concat_filas = np.concatenate((V.array_poblacion[i], V.array_poblacion[i + 1]), axis=0)
            # Matriz 10x20 potencia
            hijo2_potencia = np.concatenate((V.array_energia_molino[i], V.array_energia_molino[i + 1]), axis=0)

            sumatoria_h2 = hijo2_potencia.sum(axis=1)  # Devuelve un arreglo con la sumatoria de todas las filas
            permutacion = np.argsort(-sumatoria_h2)

            # Reordena las filas segun la sumaoria de potencias (sumatoria_h1)
            hijo2_concat_columnas = padres_concat_filas[permutacion]
            # Elimina las filas sobrantes
            hijo2 = hijo2_concat_columnas[:P.filas, :]

            V.array_poblacion[i] = hijo1
            V.array_poblacion[i + 1] = hijo2
    #            -- BORRA MOLINOS SOBRANTES (> cant_molinos)--
    borrar_molinos_extra()


def borrar_molinos_extra():
    borrar_corridas = len(V.array_poblacion)
    for i in range(borrar_corridas):
        cromosoma = V.array_poblacion[i]
        cantidad_molinos_actual = np.count_nonzero(cromosoma)

        while cantidad_molinos_actual > P.cant_molinos:
            calcula_energia_cromosoma(i)

            energia_cromosoma = np.asarray(V.array_energia_molino[i])

            # Se "achata" la matriz para poder el minimo valor
            arr_flat = energia_cromosoma.flatten()

            min_value = np.min(arr_flat[np.nonzero(arr_flat)])

            coord = np.where(energia_cromosoma == min_value)

            coord = np.asarray(coord).transpose()

            x = coord[0][0]
            y = coord[0][1]

            cromosoma[x][y] = 0
            V.array_poblacion[i] = cromosoma

            cantidad_molinos_actual -= 1


def retorna_energia(vel_viento):
    # region Constantes
    a = 21.9836777975935
    b = 4.25803634217095
    c = 598.888997473194
    d = 687.348053493969
    m = 40402603.2299475
    # endregion

    if vel_viento < 5 or vel_viento > 25:
        pot_generada = 0

    elif 13 <= vel_viento <= 25:
        pot_generada = 660

    else:
        pot_generada = d + (a - d) / (1 + (vel_viento / c) ** b) ** m

    return pot_generada


def calcula_velocidad_viento(velocidad_inicial, x):
    velocidad_final = velocidad_inicial * (1 - (2 * V.molinos.induccion_axial) / np.square(
        1 + (V.molinos.arrastre * (V.molinos.distancia_minima * x) / V.molinos.radio_estela)))
    return velocidad_final


def calcula_energia_cromosoma(ind_crom):  # Pensar para 3 molinos consecutivos
    energia = 0
    m_energia = np.zeros((P.filas, P.columnas))
    m = V.array_poblacion[ind_crom]
    # Def matriz de vientos que me arme un 10x10 con todos los valores del viento
    for i in range(P.filas):
        flag = True
        cont = 0
        for j in range(P.columnas):

            if m[i][j] == 1:  # Si hay un molino en la posición
                # Entra si el viento es puro
                if flag or P.cte_long_estela * V.molinos.diametro <= cont * V.molinos.distancia_minima:
                    flag = False
                    energia = energia + retorna_energia(P.viento_puro)
                    m_energia[i][j] = retorna_energia(P.viento_puro)
                    velocidad_anterior = P.viento_puro
                    cont = 1
                # Entra si el viento es turbulento
                else:
                    velocidad_final = calcula_velocidad_viento(velocidad_anterior, cont)
                    velocidad_anterior = velocidad_final
                    energia = energia + retorna_energia(velocidad_final)
                    m_energia[i][j] = retorna_energia(velocidad_final)
                    cont = 1
            else:
                cont += 1

    V.array_energia_molino[ind_crom] = m_energia
    return energia


def fitness():
    energia_total_pob = np.sum(V.array_energia_crom)
    for i in range(P.tam_poblacion):
        V.array_fitness[i] = V.array_energia_crom[i] / energia_total_pob


def ruleta():
    aux_poblacion = V.array_poblacion
    base = 0
    cant_casilleros = 0
    tam_nueva_poblacion = len(V.array_poblacion)
    if tam_nueva_poblacion < P.tam_poblacion:
        for elitistas in range(len(V.array_elite)):
            V.array_poblacion.append(V.array_elite[elitistas])

    for i in range(P.tam_poblacion):
        casilleros = round(V.array_fitness[i] * 1000)
        cant_casilleros = cant_casilleros + casilleros
    roulette = [0] * cant_casilleros

    for i in range(P.tam_poblacion):
        casilleros = round(V.array_fitness[i] * 1000)

        for j in range(base, base + casilleros):
            roulette[j] = i
        base = base + casilleros

    nueva_poblacion = [0] * tam_nueva_poblacion
    for i in range(tam_nueva_poblacion):
        bolilla = random.randint(0, cant_casilleros - 1)
        nueva_poblacion[i] = aux_poblacion[roulette[bolilla]]

    return nueva_poblacion


def mutacion():
    muta_corridas = len(V.array_poblacion)
    for i in range(muta_corridas):
        muta = random.random()
        if muta < P.chances_mutacion:
            x1 = random.randint(0, P.filas - 1)
            y1 = random.randint(0, P.columnas - 1)
            x2 = random.randint(0, P.filas - 1)
            y2 = random.randint(0, P.columnas - 1)
            while V.array_poblacion[i][x1][y1] != 1:
                x1 = random.randint(0, P.filas - 1)
                y1 = random.randint(0, P.columnas - 1)
            while V.array_poblacion[i][x2][y2] != 0:
                x2 = random.randint(0, P.filas - 1)
                y2 = random.randint(0, P.columnas - 1)
            V.array_poblacion[i][x1][y1] = 0
            V.array_poblacion[i][x2][y2] = 1


def elite():
    array_elitismo = [0] * P.tam_elitismo
    # Devuelve los indices de los mejores cromosomas, considerando el fitness, de mayor a menor
    indices_elitismo = np.argsort(V.array_fitness)[::-1][:P.tam_elitismo]
    for i in range(P.tam_elitismo):
        array_elitismo[i] = V.array_poblacion[indices_elitismo[i]]
    V.array_poblacion = np.delete(V.array_poblacion, indices_elitismo, 0).tolist()
    return array_elitismo
