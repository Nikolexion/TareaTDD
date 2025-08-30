from .contador_pintas import Contador_pintas
from .dado import Dado

class Apuesta:
    def __init__(self, cantidad, pinta, jugador_que_aposto = None):
        self.cantidad = cantidad
        self.pinta = pinta
        self.jugador_que_aposto = jugador_que_aposto

class ResultadoDuda:
    def __init__(self, pierde_dado):
        self.pierde_dado = pierde_dado

class ResultadoCalzar:
    def __init__(self, acierta):
        self.acierta = acierta

class ArbitroRonda:
    def __init__(self, jugador_inicial, jugadores):
        self.jugador_inicial = jugador_inicial
        self.jugadores = jugadores

    def pinta_en_string(self, apuesta):
        if isinstance(apuesta.pinta, int):
             pinta_en_string = Dado.PINTA[apuesta.pinta]
        else:
             pinta_en_string = apuesta.pinta
        return pinta_en_string

    def resolver_duda(self, apuesta, cacho, jugador_duda, obligar = False):
        pinta_en_string = self.pinta_en_string(apuesta)
        total = Contador_pintas(cacho).contar_pintas(pinta_en_string, obligar=obligar)

        if total >= apuesta.cantidad:
            pierde = jugador_duda
        else:
            pierde = apuesta.jugador_que_aposto


        return ResultadoDuda(pierde)

    def resolver_calzar(self, apuesta, cacho, jugador_calza, obligar = False):
        pinta_en_string = self.pinta_en_string(apuesta)
        total = Contador_pintas(cacho).contar_pintas(pinta_en_string, obligar=obligar)

        if total == apuesta.cantidad:
            return ResultadoCalzar(acierta =True)
        else:
            return ResultadoCalzar(acierta = False)