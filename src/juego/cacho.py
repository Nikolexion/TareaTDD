from .dado import Dado

class Cacho:
    def __init__(self):
        self.dado1 = Dado()
        self.dado1.lanzar()
        self.dado2 = Dado()
        self.dado2.lanzar()
        self.dado3 = Dado()
        self.dado3.lanzar()
        self.dado4 = Dado()
        self.dado4.lanzar()
        self.dado5 = Dado()
        self.dado5.lanzar()

        self.dados = [self.dado1, self.dado2, self.dado3, self.dado4, self.dado5]
        self.num_dados = 5

    def agitar(self):
        if self.num_dados == 0:
            return None
        for i in range(len(self.dados)):
            self.dados[i] = self.dados[i].lanzar()
        return self.dados
    
    def numero_dados(self):
        return self.num_dados

    def numero_dados_en_juego(self):
        return len(self.dados)
    
    def quitar_dado(self):
        if self.num_dados > 5:
            self.num_dados -= 1
        elif self.num_dados > 0:
            self.dados.pop()
            self.num_dados -= 1
            
    def sumar_dado(self):
        if self.num_dados < 5:
            nuevo_dado = Dado()
            self.dados.append(nuevo_dado)
        
        self.num_dados += 1
