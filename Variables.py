import Parameters as P
import Models as M

viento = [0] * 10
cromosoma_mvp = [0] * 4
array_energia_crom = [0] * P.tam_poblacion  # Se guardan los totales de energia de todos los cromosomas
array_poblacion = [0] * P.tam_poblacion  # Se guardan todos los cromosomas
array_energia_molino = [0] * P.tam_poblacion  # Se guarda la energia producida por cada molino
array_fitness = [0] * P.tam_poblacion  # Se guarda el fitness de cada cromosoma
array_minimos = [0] * P.corridas
array_maximos = [0] * P.corridas
array_promedios = [0] * P.corridas

mayor = 0
menor = 40000
promedio = 0

array_elite = [0] * P.tam_elitismo
molinos = M.Molino("GAMESA G47", 55, 47, 660)

viento[0] = M.Viento(4, 0)
viento[1] = M.Viento(5, 53)
viento[2] = M.Viento(6, 106)
viento[3] = M.Viento(7, 166)
viento[4] = M.Viento(8, 252)
viento[5] = M.Viento(9, 350)
viento[6] = M.Viento(10, 464)
viento[7] = M.Viento(11, 560)
viento[8] = M.Viento(12, 630)
viento[9] = M.Viento(25, 660)

molinos = M.Molino("GAMESA G47", 55, 47, viento)