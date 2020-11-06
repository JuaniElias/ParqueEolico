corridas = 50
tam_poblacion = 50
chances_crossover = 0.80
chances_mutacion = 0.05
porc_elitismo = 0.1
cte_long_estela = 12  # Podemos jugar con este valor
cant_molinos = 25
viento_puro = 14

# Parametros del Terreno
rugosidad = 0.0024
filas = 10
columnas = 10
# # altitud = 0
# # angulo_inclinacion_promedio = 0


tam_elitismo = int(tam_poblacion * porc_elitismo)
tam_elitismo = tam_elitismo if tam_elitismo % 2 == 0 else tam_elitismo + 1
