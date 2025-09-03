from src.servicios.generador_aleatorio import GeneradorAleatorio

class Dado:
    """
    Clase que representa un dado con valores personalizados y nombres de pinta.
    Atributos:
        PINTA (dict): Diccionario que asocia cada valor del dado con su nombre de pinta.
        generador: Instancia responsable de generar valores aleatorios para el dado.
        valor: Último valor obtenido al lanzar el dado.
    Métodos:
        __init__(generador=None): Inicializa el dado con un generador aleatorio opcional.
        lanzar(): Lanza el dado y retorna el valor generado.
        pinta(): Retorna el nombre de la pinta correspondiente al valor actual del dado.
    """
    PINTA = {
    1: "As",
    2: "Tonto",
    3: "Tren",
    4: "Cuadra",
    5: "Quina",
    6: "Sexto"
}
    def __init__(self, generador = None):
        """
        Inicializa el dado con un generador aleatorio opcional.
        """
        if generador is None:
            self.generador = GeneradorAleatorio()
        elif callable(generador):
            self.generador = GeneradorAleatorio(generador)
        else:
            self.generador = generador
        self.valor = None
    
    def lanzar(self):
        """
        Lanza el dado y retorna el valor generado.

        Returns:
            int: El valor generado al lanzar el dado.
        """
        self.valor = self.generador.generar()
        return self.valor
    
    def pinta(self):
        """
        Retorna el nombre de la pinta correspondiente al valor actual del dado.

        Returns:
            str: El nombre de la pinta del dado.
        """
        return self.PINTA[self.valor]
        
