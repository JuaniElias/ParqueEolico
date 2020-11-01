import Parameters as P
import Models as M

cromosoma_mvp = [0] * 5
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
molinos = M.Molino("GAMESA G47", 55, 47)

