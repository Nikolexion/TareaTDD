import pytest

# 1. Para iniciar el juego, todos los jugadores lanzan un dado. El mayor parte, y en caso de empate, se vuelven a tirar los dados
# 2. El jugador que parte decide el flujo de juego (horario o antihorario)
# 3. El jugador que pierde o gana un dado empieza en la siguiente ronda
# 4.

import pytest
from src.juego.jugador import Jugador
from src.juego.gestor_partida import GestorPartida

def test_inicializar_lista_de_jugadores():
    jugadores = [Jugador("hugo"), Jugador("julio"), Jugador("geoffrey")]
    gestor = GestorPartida(jugadores)
    assert gestor.jugadores == jugadores

def test_determinar_jugador_inicial_de_juego(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [4, 6, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugadores = [mocker.Mock(nombre="hugo"), mocker.Mock(nombre="julio"), mocker.Mock(nombre="geoffrey")]
    gestor = GestorPartida(jugadores)

    gestor.determinar_jugador_inicial()
    assert gestor.jugador_inicial == jugadores[1]

def test_jugador_que_inicia_proxima_ronda():
    jugadores = [Jugador("hugo"), Jugador("julio"), Jugador("geoffrey")]
    gestor = GestorPartida(jugadores)

    #jugador que pierde o gana un dado empieza la proxima ronda
    jugador_afectado = jugadores[1]
    gestor.establecer_jugador_afectado(jugador_afectado)

    gestor.iniciar_ronda()
    assert gestor.jugador_inicial == jugador_afectado

def test_flujo_turnos_desde_jugador():
    jugadores = [Jugador("hugo"), Jugador("julio"), Jugador("geoffrey")]
    gestor = GestorPartida(jugadores)

    #jugador inicial de ronda, no de juego
    gestor.establecer_jugador_afectado(jugadores[2])
    gestor.definir_sentido("horario") #sentido de juego
    gestor.iniciar_ronda()

    assert gestor.obtener_jugador_actual() == jugadores[2]
    gestor.avanzar_turno()
    assert gestor.obtener_jugador_actual() == jugadores[0]
    gestor.avanzar_turno()
    assert gestor.obtener_jugador_actual() == jugadores[1]

def test_detectar_jugador_con_un_dado_valido():
    jugador = Jugador("camila")
    jugador.cacho.dados = jugador.cacho.dados[:1]
    jugador.cacho.num_dados = 1

    gestor = GestorPartida([jugador])
    gestor.verificar_reglas_especiales(jugador)

    assert jugador.reglas_especiales is True

def test_detectar_jugador_con_un_dado_invalido():
    jugador = Jugador("camila")
    gestor = GestorPartida([jugador])
    gestor.verificar_reglas_especiales(jugador)

    assert not getattr(jugador, "reglas_especiales", False)


#caso en que hay empate en el lanzamiento al empezar la partida de juego
def test_repetir_lanzamiento_si_empate(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [6, 6, 3, 4, 5]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugadores = [mocker.Mock(nombre="hugo"), mocker.Mock(nombre="julio"), mocker.Mock(nombre="geoffrey")]
    gestor = GestorPartida(jugadores)

    gestor.determinar_jugador_inicial()
    assert gestor.jugador_inicial == jugadores[1]  #julio gana el desempate (valor 5)


def test_flujo_turnos_sentido_horario():
    jugadores = [Jugador("cecilia"), Jugador("geoffrey"), Jugador("julio"), Jugador("hugo")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[1]
    gestor.definir_sentido("horario")

    orden = gestor.obtener_orden_turnos()
    assert orden == [jugadores[1], jugadores[2], jugadores[3], jugadores[0]]

def test_flujo_turnos_sentido_antihorario():
    jugadores = [Jugador("cecilia"), Jugador("geoffrey"), Jugador("julio"), Jugador("hugo")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[2]
    gestor.definir_sentido("antihorario")

    orden = gestor.obtener_orden_turnos()
    assert orden == [jugadores[2], jugadores[1], jugadores[0], jugadores[3]]


#si solo un jugador tiene dados
def test_partida_terminada():
    jugador1 = Jugador("geoffrey")
    jugador2 = Jugador("julio")
    jugador3 = Jugador("hugo")

    jugador2.cacho.dados = []
    jugador3.cacho.dados = []

    gestor = GestorPartida([jugador1, jugador2, jugador3])
    assert gestor.partida_terminada() is True
    
    
#se juega una partida completa y debe quedar un único ganador
#def test_jugar_partida():
    
