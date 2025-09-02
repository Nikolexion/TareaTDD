from src.juego.gestor_partida import GestorPartida
from src.juego.jugador import JugadorBot

jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
gestor = GestorPartida(jugadores)

gestor.iniciar_partida()