from .cacho import Cacho

class Contador_pintas:
    def __init__(self, cacho: Cacho):
        """
        Inicializa el contador de pintas con un objeto Cacho.
        """
        self.cacho = cacho

    def contar_pintas(self, pinta: str, obligar: bool):
        """
        Cuenta las pintas de un tipo específico en el cacho.

        Args:
            pinta (str): El nombre de la pinta a contar.
            obligar (bool): Si se deben contar los ases como la pinta especificada.

        Returns:
            int: La cantidad de pintas contadas.
        """
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
