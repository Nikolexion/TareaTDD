import random

class GeneradorAleatorio:
    """
    Genera números aleatorios entre 1 y 6.

    Permite inyectar una función generadora para pruebas.
    Si no se entrega un generador, usa `random.randint(1, 6)`.

    """

    def __init__(self, generador_aleatorio=None):
        """Inicializa el generador."""
        # Si no se entrega un generador, usar randint(1,6)
        if generador_aleatorio is None:
            self.generador_aleatorio = lambda: random.randint(1, 6)
        else:
            self.generador_aleatorio = generador_aleatorio

    def generar(self):
        """Devuelve un número entero generado por la función interna."""
        return self.generador_aleatorio()
