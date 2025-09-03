from .dado import Dado

class Cacho:
    def __init__(self):
        """
        Inicialización de los dados dentro del cacho
        """
        self.dado1 = Dado()
        self.dado2 = Dado()
        self.dado3 = Dado()
        self.dado4 = Dado()
        self.dado5 = Dado()

        self.dados = [self.dado1, self.dado2, self.dado3, self.dado4, self.dado5]
        for dado in self.dados:
            dado.lanzar()
        self.num_dados = 5

    def agitar(self):
        """
        Agitar todos los dados actuales, si hay dados en juego

        Returns:
            list[Dado]: La lista de dados después de lanzar, o None si no hay dados en juego.
        """
        if self.num_dados == 0:
            return None
        for dado in self.dados:
            dado.lanzar()
        return self.dados
    
    def numero_dados(self):
        """
        Devuelve el número de dados utilizados en el juego.

        Returns:
            int: El número de dados.
        """
        return self.num_dados

    def numero_dados_en_juego(self):
        """
        Retorna el numero de dados actualmente en juego.

        Returns:
            int: La cantidad de dados en la lista 'dados'.
        """
        return len(self.dados)
    
    def quitar_dado(self):
        """
        Elimina un dado del juego si hay más de 0 dados en juego.
        """
        if self.num_dados > 5:
            self.num_dados -= 1
        elif self.num_dados > 0:
            self.dados.pop()
            self.num_dados -= 1
            
    def sumar_dado(self):
        """
        Agrega un dado al juego si hay menos de 5 dados en juego.
        """
        if self.num_dados < 5:
            nuevo_dado = Dado()
            self.dados.append(nuevo_dado)
        
        self.num_dados += 1
