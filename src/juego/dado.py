import random

class Dado:
    def __init__(self):
        self.valor = None
    
    def lanzar(self):
        self.valor = random.randint(1, 6)
        return self.valor