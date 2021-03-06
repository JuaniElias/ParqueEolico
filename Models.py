import Parameters as P
import numpy as np


class Molino:
    def __init__(self, modelo, altura, diametro):
        self.modelo = modelo
        self.altura = altura
        self.diametro = diametro
        self.distancia_minima = 2 * diametro
        self.arrastre = 1 / (2 * np.log(altura / P.rugosidad))
        self.induccion_axial = 1 / 3
        self.radio_estela = 2 * diametro  # diametro/2 * 4 (valor maximo de gama), preguntar


class Terreno:
    def __init__(self, altitud, rugosidad, angulo_inclinacion_promedio):
        self.altitud = altitud
        self.rugosidad = rugosidad
        self.angulo_inclinacion_promedio = angulo_inclinacion_promedio
