from .contador_pintas import Contador_pintas
from .dado import Dado

class Apuesta:
    def __init__(self, cantidad, pinta):
        self.cantidad = cantidad
        self.pinta = pinta

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

    def resolver_duda(self, apuesta, cacho, jugador_duda, jugador_apuesta, obligar = False):
        #Para usar contador pintas
        if isinstance(apuesta.pinta, int):
            pinta_en_string = Dado.PINTA[apuesta.pinta]
        else:
            pinta_en_string = apuesta.pinta

        total = Contador_pintas(cacho).contar_pintas(pinta_en_string, obligar=obligar)

        if total >= apuesta.cantidad:
            pierde = jugador_duda
        else:
            pierde = jugador_apuesta

        return ResultadoDuda(pierde)

    def resolver_calzar(self, apuesta, cacho, jugador_calza, jugador_apuesta, obligar = False):
        if isinstance(apuesta.pinta, int):
            pinta_en_string = Dado.PINTA[apuesta.pinta]
        else:
            pinta_en_string = apuesta.pinta

        total = Contador_pintas(cacho).contar_pintas(pinta_en_string, obligar=obligar)

        if total == apuesta.cantidad:
            return ResultadoCalzar(acierta =True)
        else:
            ResultadoCalzar(acierta = False)