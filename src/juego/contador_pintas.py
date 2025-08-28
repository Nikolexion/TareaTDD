from .cacho import Cacho

class Contador_pintas:
    def __init__(self, cacho: Cacho):
        self.cacho = cacho

    def contar_pintas(self, pinta: str, obligar: bool):
        self.obligar = obligar
        cont = 0
        ases = 0
        for dado in self.cacho.dados:
            if dado.pinta() == "As":
                ases += 1
            elif dado.pinta() == pinta:
                cont += 1
            
        if not self.obligar:
            cont += ases
        return cont
