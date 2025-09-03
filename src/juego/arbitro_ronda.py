from .contador_pintas import Contador_pintas
from .dado import Dado
import math

class Apuesta:
    """Modelo simple de una apuesta."""
    def __init__(self, cantidad, pinta, jugador_que_aposto = None):
        self.cantidad = cantidad
        self.pinta = pinta
        self.jugador_que_aposto = jugador_que_aposto


class ResultadoDuda:
    """Resultado de resolver una 'duda'."""
    def __init__(self, pierde_dado):
        self.pierde_dado = pierde_dado


class ResultadoCalzar:
    """Resultado de resolver un 'calzar'."""
    def __init__(self, acierta, pierden_dado=None, recupera_jugador=None):
        if pierden_dado is None:
            pierden_dado = []
        self.acierta = acierta
        self.pierden_dado = pierden_dado
        self.recupera_jugador = recupera_jugador


class ArbitroRonda:
    """Arbitra la resolución de jugadas dentro de una ronda (dudar / calzar) y utilidades de apuesta."""
    def __init__(self, jugador_inicial, jugadores):
        self.jugador_inicial = jugador_inicial
        self.jugadores = jugadores

    def pinta_en_string(self, apuesta):
        """Normaliza la pinta a string usando el mapa Dado.PINTA si viene como int."""
        if isinstance(apuesta.pinta, int):
             pinta_en_string = Dado.PINTA[apuesta.pinta]
        else:
             pinta_en_string = apuesta.pinta
        return pinta_en_string

    def resolver_duda(self, apuesta, cacho, jugador_duda, obligar=False):
        """Resuelve una 'duda"""
        pinta_en_string = self.pinta_en_string(apuesta)

        total = 0
        #Suma el total de pintas
        for jugador in self.jugadores:
            contador = Contador_pintas(jugador.cacho)
            total += contador.contar_pintas(pinta_en_string, obligar=obligar)

        if total >= apuesta.cantidad:
            pierde = jugador_duda
        else:
            pierde = apuesta.jugador_que_aposto
        #Devuelve quien pierde un daod
        return ResultadoDuda(pierde)

    def puede_calzar(self, apuesta, jugador_calza):
        """Valida si 'calzar' está permitido según reglas del dudo"""
        if not isinstance(apuesta.cantidad, int) or apuesta.cantidad < 1:
            raise ValueError()
        #Calcula el total de dados en juego sumando jugador por jugador
        total_dados_en_juego = 0
        for jugador in self.jugadores:
            dados_jugador = getattr(jugador, "num_dados", None)
            if dados_jugador is None:
                cacho = getattr(jugador, "cacho", None)
                if cacho is not None and hasattr(cacho, "numero_dados"):
                    dados_jugador = cacho.numero_dados()
            #valida que sea un entero no negativo
            if not isinstance(dados_jugador, int) or dados_jugador < 0:
                raise ValueError()
            total_dados_en_juego += dados_jugador
        #Si no hay dados en juego, situación invalida
        if total_dados_en_juego <= 0:
            raise ValueError()
        #Obtiene los dados del jugador que intenta calzar
        dados_calzador = getattr(jugador_calza, "num_dados", None)
        if dados_calzador is None:
            cacho = getattr(jugador_calza, "cacho", None)
            if cacho is not None and hasattr(cacho, "numero_dados"):
                dados_calzador = cacho.numero_dados()
        #Para poder calzar, el jugador debe tener al menos 1 dado
        if not isinstance(dados_calzador, int) or dados_calzador < 1:
            raise ValueError()

        #Mitad redondeada hacia arriba
        mitad_redondeada = math.ceil(total_dados_en_juego / 2)

        #Permitido por cantidad o por tener un solo dado
        if apuesta.cantidad >= mitad_redondeada:
            return True
        if dados_calzador == 1:
            return True
        return False

    def resolver_calzar(self, apuesta, cacho, jugador_calza, obligar=False):
        """Resuelve un 'calzar'."""
        if not self.puede_calzar(apuesta, jugador_calza):
            raise ValueError()
        #normaliza la pinta
        pinta_en_string = self.pinta_en_string(apuesta)
        #Cuenta las pintas con funcion Contador_pintas
        total = Contador_pintas(cacho).contar_pintas(pinta_en_string, obligar=obligar)
        #si calza, recupera el que calza
        if total == apuesta.cantidad:
            return ResultadoCalzar(acierta=True, pierden_dado=[], recupera_jugador=jugador_calza)
        #Si no, falla y pierde un dado el que calza
        else:
            return ResultadoCalzar(acierta=False, pierden_dado=[jugador_calza])
