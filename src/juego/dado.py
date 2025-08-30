from src.servicios.generador_aleatorio import GeneradorAleatorio

class Dado:
    PINTA = {
    1: "As",
    2: "Tonto",
    3: "Tren",
    4: "Cuadra",
    5: "Quina",
    6: "Sexto"
}
    def __init__(self, generador = None):
        if generador is None:
            self.generador = GeneradorAleatorio()
        elif callable(generador):
            self.generador = GeneradorAleatorio(generador)
        else:
            self.generador = generador
        self.valor = None
    
    def lanzar(self):
        self.valor = self.generador.generar()
        return self.valor
    
    def pinta(self):
        return self.PINTA[self.valor]
        
