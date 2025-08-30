import random

import random

class GeneradorAleatorio:
    def __init__(self, generador_aleatorio=None):
        if generador_aleatorio is None:
            self.generador_aleatorio = lambda: random.randint(1, 6)
        else:
            self.generador_aleatorio = generador_aleatorio

    def generar(self):
        return self.generador_aleatorio()
