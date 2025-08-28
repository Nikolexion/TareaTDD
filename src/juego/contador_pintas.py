class Contador_pintas:
    def __init__(self, obligar, cacho):
        self.obligar = obligar
        self.cacho = cacho
        self.contador = [0, 0, 0, 0, 0, 0]

    def contar_pintas(self):
        for dado in self.cacho.dados:
            if dado.pinta() == "As":
                self.contador[0] += 1
            elif dado.pinta() == "Tonto":
                self.contador[1] += 1
            elif dado.pinta() == "Tren":
                self.contador[2] += 1
            elif dado.pinta() == "Cuadra":
                self.contador[3] += 1
            elif dado.pinta() == "Quina":
                self.contador[4] += 1
            elif dado.pinta() == "Sexto":
                self.contador[5] += 1

        if not self.obligar:
            for contador in range(1, 6):
                self.contador[contador] += self.contador[0]
        return self.contador
