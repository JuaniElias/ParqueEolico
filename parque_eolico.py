import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors

corridas = 30
tam_poblacion = 100
rugosidad = 0.0024
chances_crossover = 2
chances_mutacion = 0.20
filas = 10
columnas = 10
cte_long_estela = 12  # Podemos jugar con este valor
cant_molinos = 25
viento_puro = 15
porc_elitismo = 0.1

tam_elitismo = int(tam_poblacion * porc_elitismo)
tam_elitismo = tam_elitismo if tam_elitismo % 2 == 0 else tam_elitismo + 1

viento = [0] * 10
cromosoma_mvp = [0] * 2
array_energia_crom = [0] * tam_poblacion  # Se guardan los totales de energia de todos los cromosomas
array_poblacion = [0] * tam_poblacion  # Se guardan todos los cromosomas
array_energia_molino = [0] * tam_poblacion  # Se guarda la energia producida por cada molino
array_fitness = [0] * tam_poblacion  # Se guarda el fitness de cada cromosoma
array_minimos = [0] * corridas
array_maximos = [0] * corridas
array_promedios = [0] * corridas


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
    global array_poblacion
    aux_poblacion = array_poblacion
    base = 0
    cant_casilleros = 0
    tam_nueva_poblacion = len(array_poblacion)
    if tam_nueva_poblacion < tam_poblacion:
        for elitistas in range(len(array_elite)):
            array_poblacion.append(array_elite[elitistas])

    for i in range(tam_poblacion):
        casilleros = round(array_fitness[i] * 1000)
        cant_casilleros = cant_casilleros + casilleros
    roulette = [0] * cant_casilleros

    for i in range(tam_poblacion):
        casilleros = round(array_fitness[i] * 1000)

        for j in range(base, base + casilleros):
            roulette[j] = i
        base = base + casilleros

    nueva_poblacion = [0] * tam_nueva_poblacion
    for i in range(tam_nueva_poblacion):
        bolilla = random.randint(0, cant_casilleros - 1)
        nueva_poblacion[i] = aux_poblacion[roulette[bolilla]]

    return nueva_poblacion


def retorna_energia(velocidad):
    velocidad = round(velocidad)
    for i in range(filas):
        if velocidad == molinos.velocidad_potencia[i].velocidad:
            return molinos.velocidad_potencia[i].potencia
    if 13 <= velocidad <= 25:
        return molinos.velocidad_potencia[9].potencia
    elif velocidad > 25 or 0 <= velocidad < 4:
        return molinos.velocidad_potencia[0].potencia


def calcula_velocidad_viento(velocidad_inicial, x):
    velocidad_final = velocidad_inicial * (1 - (2 * molinos.induccion_axial) / np.square(
        1 + (molinos.arrastre * (molinos.distancia_minima * x) / molinos.radio_estela)))
    return velocidad_final


def calcula_energia_cromosoma(ind_crom):  # Pensar para 3 molinos consecutivos
    energia = 0
    m_energia = np.zeros((filas, columnas))
    m = array_poblacion[ind_crom]
    # Def matriz de vientos que me arme un 10x10 con todos los valores del viento
    for i in range(filas):
        flag = True
        cont = 0
        for j in range(columnas):

            if m[i][j] == 1:  # Si hay un molino en la posición
                # Entra si el viento es puro
                if flag or cte_long_estela * molinos.diametro <= cont * molinos.distancia_minima:
                    flag = False
                    energia = energia + retorna_energia(viento_puro)
                    m_energia[i][j] = retorna_energia(viento_puro)
                    velocidad_anterior = viento_puro
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

    array_energia_molino[ind_crom] = m_energia
    return energia


def fitness():
    energia_total_pob = np.sum(array_energia_crom)
    for i in range(tam_poblacion):
        array_fitness[i] = array_energia_crom[i] / energia_total_pob


def poblacion_inicial():
    for i in range(tam_poblacion):
        m = np.zeros((filas, columnas), dtype=int)
        cont = 0
        while cont < 25:
            x = random.randint(0, filas - 1)
            y = random.randint(0, columnas - 1)
            if m[x][y] == 0:
                m[x][y] = 1
                cont = cont + 1
        array_poblacion[i] = m


def borrar_molinos_extra():
    borrar_corridas = len(array_poblacion)
    for i in range(borrar_corridas):
        cromosoma = array_poblacion[i]
        cantidad_molinos_actual = np.count_nonzero(cromosoma)

        while cantidad_molinos_actual > cant_molinos:
            calcula_energia_cromosoma(i)

            energia_cromosoma = np.asarray(array_energia_molino[i])

            # Se "achata" la matriz para poder el minimo valor
            arr_flat = energia_cromosoma.flatten()

            min_value = np.min(arr_flat[np.nonzero(arr_flat)])

            coord = np.where(energia_cromosoma == min_value)

            coord = np.asarray(coord).transpose()

            x = coord[0][0]
            y = coord[0][1]

            cromosoma[x][y] = 0
            array_poblacion[i] = cromosoma

            cantidad_molinos_actual -= 1


def crossover():
    cros_corridas = len(array_poblacion)
    for i in range(0, cros_corridas, 2):
        cros = random.random()

        if cros < chances_crossover:
            #                               -- CROSSOVER POR COLUMNAS (Hijo 1)--
            # Matriz 20x10 molinos
            padres_concat_columnas = np.concatenate((array_poblacion[i], array_poblacion[i + 1]), axis=1)
            # Matriz 20x10 potencia
            hijo1_potencia = np.concatenate((array_energia_molino[i], array_energia_molino[i + 1]), axis=1)

            sumatoria_h1 = hijo1_potencia.sum(axis=0)  # Devuelve un arreglo con la sumatoria de todas las columnas
            permutacion = np.argsort(-sumatoria_h1)

            # Reordena las columnas segun la sumaoria de potencias (sumatoria_h1)
            hijo1_concat_columnas = padres_concat_columnas[:, permutacion]
            # Elimina las columnas sobrantes
            hijo1 = hijo1_concat_columnas[:, :columnas]

            #                                 -- CROSSOVER POR FILAS (Hijo 2)--
            # Matriz 10x20 molinos
            padres_concat_filas = np.concatenate((array_poblacion[i], array_poblacion[i + 1]), axis=0)
            # Matriz 10x20 potencia
            hijo2_potencia = np.concatenate((array_energia_molino[i], array_energia_molino[i + 1]), axis=0)

            sumatoria_h2 = hijo2_potencia.sum(axis=1)  # Devuelve un arreglo con la sumatoria de todas las filas
            permutacion = np.argsort(-sumatoria_h2)

            # Reordena las filas segun la sumaoria de potencias (sumatoria_h1)
            hijo2_concat_columnas = padres_concat_filas[permutacion]
            # Elimina las filas sobrantes
            hijo2 = hijo2_concat_columnas[:filas, :]

            array_poblacion[i] = hijo1
            array_poblacion[i + 1] = hijo2
    #            -- BORRA MOLINOS SOBRANTES (> cant_molinos)--
    borrar_molinos_extra()


def mutacion():
    muta_corridas = len(array_poblacion)
    for i in range(muta_corridas):
        muta = random.random()
        if muta < chances_mutacion:
            x1 = random.randint(0, filas - 1)
            y1 = random.randint(0, columnas - 1)
            x2 = random.randint(0, filas - 1)
            y2 = random.randint(0, columnas - 1)
            while array_poblacion[i][x1][y1] != 1:
                x1 = random.randint(0, filas - 1)
                y1 = random.randint(0, columnas - 1)
            while array_poblacion[i][x2][y2] != 0:
                x2 = random.randint(0, filas - 1)
                y2 = random.randint(0, columnas - 1)
            array_poblacion[i][x1][y1] = 0
            array_poblacion[i][x2][y2] = 1


def elite():
    global array_poblacion
    array_elitismo = [0] * tam_elitismo
    # Devuelve los indices de los mejores cromosomas, considerando el fitness, de mayor a menor
    indices_elitismo = np.argsort(array_fitness)[::-1][:tam_elitismo]
    for i in range(tam_elitismo):
        array_elitismo[i] = array_poblacion[indices_elitismo[i]]
    array_poblacion = np.delete(array_poblacion, indices_elitismo, 0).tolist()
    return array_elitismo


def asigna_mvp():
    global cromosoma_mvp

    indice_mvp = np.argmax(array_energia_crom)
    if cromosoma_mvp[1] < array_energia_crom[indice_mvp]:
        cromosoma_mvp[0] = array_poblacion[indice_mvp]
        cromosoma_mvp[1] = array_energia_crom[indice_mvp]


def mayor_menor_promedio():
    global mayor
    global menor
    global promedio

    for i in range(tam_poblacion):
        energia = calcula_energia_cromosoma(i)
        promedio += energia
        if energia > mayor:
            mayor = energia

        if energia < menor:
            menor = energia


def mostrar_grafica():
    plt.plot(grafica, array_maximos, 'r-', label='Maximo')
    plt.plot(grafica, array_minimos, 'b-', label='Minimo')
    plt.plot(grafica, array_promedios, 'g-', label='Promedio')
    plt.xlabel('Corridas')
    plt.ylabel('Distancia', multialignment='center')
    plt.legend()
    plt.show()


# resp = input('Quiere hacer elitismo (s/n): ')

resp = 's'
grafica = np.linspace(0, corridas, corridas)

poblacion_inicial()
cromosoma_mvp[1] = 0
for cor in range(corridas):

    mayor = 0
    menor = 40000
    promedio = 0

    for k in range(tam_poblacion):
        array_energia_crom[k] = calcula_energia_cromosoma(k)
    fitness()
    if resp == 's' or resp == 'S':
        array_elite = elite()
    crossover()
    mutacion()
    array_poblacion = ruleta()
    if resp == 's' or resp == 'S':
        for eli in range(len(array_elite)):
            array_poblacion.append(array_elite[eli])

    array_poblacion = np.random.permutation(array_poblacion).tolist()

    asigna_mvp()
    mayor_menor_promedio()

    array_maximos[cor] = mayor
    array_minimos[cor] = menor
    array_promedios[cor] = promedio / tam_poblacion

for dou in range(filas):
    print(cromosoma_mvp[0][dou])

for k in range(tam_poblacion):
    array_energia_crom[k] = calcula_energia_cromosoma(k)
fitness()

print(cromosoma_mvp[1])


mostrar_grafica()

colormap = colors.ListedColormap(["#90E577", "grey"])
plt.figure(figsize=(5, 5))
plt.imshow(cromosoma_mvp[0], cmap=colormap)
plt.axis('off')
plt.show()

