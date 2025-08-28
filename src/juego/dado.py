import random

class Dado:
    PINTA = {
    1: "As",
    2: "Tonto",
    3: "Tren",
    4: "Cuadra",
    5: "Quina",
    6: "Sexto"
}
    def __init__(self):
        self.valor = None
    
    def lanzar(self):
        self.valor = random.randint(1, 6)
        return self.valor
    
    def pinta(self):
        return self.PINTA[self.valor]
        
