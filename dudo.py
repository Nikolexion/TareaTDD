from src.juego.gestor_partida import GestorPartida
from src.juego.jugador import JugadorBot, JugadorHumano

#opcional
jugadorHumano = JugadorHumano("apollo")

jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey"), jugadorHumano]
gestor = GestorPartida(jugadores)

gestor.iniciar_partida()