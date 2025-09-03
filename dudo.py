from src.juego.gestor_partida import GestorPartida
from src.juego.jugador import JugadorBot, JugadorHumano

opcion = input("¿Quieres jugar tú mismo (1) o ver una partida automática de bots (2)? Ingresa 1 o 2: ")
if opcion == "1":
    jugadorHumano = JugadorHumano("apollo")
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey"), jugadorHumano]
else:
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey"), JugadorBot("apollo")]

gestor = GestorPartida(jugadores)

gestor.iniciar_partida()