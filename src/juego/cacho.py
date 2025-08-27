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
        for i in range(len(self.dados)):
            self.dados[i] = self.dados[i].lanzar()
        return self.dados
    
    def numero_dados(self):
        return len(self.dados)
    
    def quitar_dado(self):
        if self.numero_dados() > 0:
            self.dados.pop()
            