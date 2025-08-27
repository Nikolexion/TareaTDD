from .dado import Dado

class Cacho:
    def __init__(self):
        self.dado1 = Dado()
        self.dado2 = Dado()
        self.dado3 = Dado()
        self.dado4 = Dado()
        self.dado5 = Dado()
        self.dados = [self.dado1, self.dado2, self.dado3, self.dado4, self.dado5]

    def agitar(self):
        self.dados[0] = self.dado1.lanzar()
        self.dados[1] = self.dado2.lanzar()
        self.dados[2] = self.dado3.lanzar()
        self.dados[3] = self.dado4.lanzar()
        self.dados[4] = self.dado5.lanzar()
        return self.dados