import random

from src.juego.jugador import Jugador
from src.juego.dado import Dado

class GestorPartida:
    def __init__(self, jugadores: Jugador):
        self.jugadores = jugadores
        self.jugador_inicial = None
        self.sentido = "horario" #sentido de juego
        self.turno_index = 0
        self.jugador_afectado = None #referencia a jugador que pierde o gana un dado
        self.orden_turnos = []

    def establecer_jugador_afectado(self, jugador: Jugador):
        self.jugador_afectado = jugador

    def definir_sentido(self, sentido: str):
        if sentido not in ["horario", "antihorario"]:
            raise ValueError("Sentido debe ser 'horario' o 'antihorario'")
        self.sentido = sentido

    def iniciar_ronda(self):
        #si hay jugador afectado, se define como el que inicia la ronda
        if self.jugador_afectado:
            self.jugador_inicial = self.jugador_afectado
        elif self.jugador_inicial is None:
            raise ValueError("Debe determinarse el jugador inicial antes de iniciar la partida")

        self.orden_turnos = self.obtener_orden_turnos()
        self.turno_index = 0
        self.jugador_afectado = None

    def obtener_orden_turnos(self):
        idx = self.jugadores.index(self.jugador_inicial)
        if self.sentido == "horario":
            return self.jugadores[idx:] + self.jugadores[:idx]
        else:
            return list(reversed(self.jugadores[:idx+1])) + list(reversed(self.jugadores[idx+1:]))

    def obtener_jugador_actual(self):
        return self.orden_turnos[self.turno_index]

    def avanzar_turno(self):
        self.turno_index = (self.turno_index + 1) % len(self.orden_turnos)

    def verificar_reglas_especiales(self, jugador):
        num_dados = jugador.cacho.numero_dados()
        if num_dados == 1:
            jugador.reglas_especiales = True

    #para determinar el jugador que empieza la partida y el sentido de juego
    def determinar_jugador_inicial(self):
        tiradas = {}
        while True:
            tiradas.clear()
            max_valor = -1
            for jugador in self.jugadores:
                valor = Dado().lanzar()
                tiradas.setdefault(valor, []).append(jugador)
                max_valor = max(max_valor, valor)

            if len(tiradas[max_valor]) == 1:
                self.jugador_inicial = tiradas[max_valor][0]
                self.definir_sentido(self.jugador_inicial.elegir_sentido()) #se elije el sentido
                break
            # en caso de empate, se repite solo entre los empatados
            self.jugadores = tiradas[max_valor]

    def partida_terminada(self):
        jugadores_activos = [j for j in self.jugadores if j.cacho.numero_dados() > 0]
        return len(jugadores_activos) == 1
    
    def iniciar_partida(self):
        if len(self.jugadores) < 2:
            raise ValueError("Se requieren al menos 2 jugadores para iniciar la partida")

        self.determinar_jugador_inicial()
        self.iniciar_ronda()