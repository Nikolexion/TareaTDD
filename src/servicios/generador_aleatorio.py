import random

class GeneradorAleatorio:

    def __init__(self, generador_aleatorio =None):
        self.generador_aleatorio = generador_aleatorio or (lambda: random.randint(1,6))