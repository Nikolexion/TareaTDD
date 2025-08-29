from .contador_pintas import Contador_pintas
from .dado import Dado
from .cacho import Cacho

class Apuesta:
    def __init__(self, cantidad, pinta):
        self.cantidad = cantidad
        self.pinta = pinta

class ResultadoDuda:
    def __init__(self, pierde_dado):
        self.pierde_dado = pierde_dado


class ArbitroRonda:
    def __init__(self, jugador_inicial, jugadores):
        self.jugador_inicial = jugador_inicial
        self.jugadores = jugadores

    def resolver_duda(self, apuesta, caras_mesa, player_duda, player_apuesta):
        #Para usar contador pintas
        if isinstance(apuesta.pinta, int):
            pinta_en_string = Dado.PINTA[apuesta.pinta]
        else:
            pinta_en_string = apuesta.pinta

        c = Cacho()
        c.dados = []
        for cara in caras_mesa:
            d = Dado()
            d.valor = cara
            c.dados.append(d)
        c.num_dados = len(c.dados)
        #falso por mientras
        total = Contador_pintas(c).contar_pintas(pinta_en_string, obligar=False)

        if total >= apuesta.cantidad:
            pierde = player_duda
        else:
            pierde = player_apuesta

        return ResultadoDuda(pierde)