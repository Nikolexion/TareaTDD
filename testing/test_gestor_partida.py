import pytest

# 1. Para iniciar el juego, todos los jugadores lanzan un dado. El mayor parte, y en caso de empate, se vuelven a tirar los dados
# 2. El jugador que parte decide el flujo de juego (horario o antihorario)
# 3. El jugador que pierde o gana un dado empieza en la siguiente ronda
# 4.

import pytest
from src.juego.jugador import JugadorBot
from src.juego.gestor_partida import GestorPartida
from src.juego.arbitro_ronda import Apuesta
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.dado import Dado
from src.juego.contador_pintas import Contador_pintas

def test_inicializar_lista_de_jugadores():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)
    assert gestor.jugadores == jugadores

def test_determinar_jugador_inicial_de_juego(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [4, 6, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugadores = [mocker.Mock(nombre="hugo"), mocker.Mock(nombre="julio"), mocker.Mock(nombre="geoffrey")]
    jugadores[1].elegir_sentido.return_value = "antihorario"
    
    gestor = GestorPartida(jugadores)

    gestor.determinar_jugador_inicial()
    assert gestor.jugador_inicial == jugadores[1]

def test_jugador_que_inicia_proxima_ronda():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)

    gestor.establecer_jugador_afectado(jugadores[1])
    gestor.iniciar_ronda()
    assert gestor.jugador_inicial == jugadores[1]

def test_flujo_turnos_desde_jugador():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)

    gestor.establecer_jugador_afectado(jugadores[2])
    gestor.definir_sentido("horario")
    gestor.iniciar_ronda()

    assert gestor.obtener_jugador_actual() == jugadores[2]
    gestor.avanzar_turno()
    assert gestor.obtener_jugador_actual() == jugadores[0]
    gestor.avanzar_turno()
    assert gestor.obtener_jugador_actual() == jugadores[1]

def test_detectar_jugador_con_un_dado_valido():
    jugador = JugadorBot("camila")
    jugador.cacho.dados = jugador.cacho.dados[:1]
    jugador.cacho.num_dados = 1

    gestor = GestorPartida([jugador])
    gestor.verificar_reglas_especiales(jugador)
    assert jugador.reglas_especiales is True

def test_detectar_jugador_con_un_dado_invalido():
    jugador = JugadorBot("camila")
    gestor = GestorPartida([jugador])
    gestor.verificar_reglas_especiales(jugador)
    assert not getattr(jugador, "reglas_especiales", False)

def test_repetir_lanzamiento_si_empate(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [6, 6, 3, 4, 5]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugadores = [mocker.Mock(nombre="hugo"), mocker.Mock(nombre="julio"), mocker.Mock(nombre="geoffrey")]
    jugadores[1].elegir_sentido.return_value = "horario"
    
    gestor = GestorPartida(jugadores)
    gestor.determinar_jugador_inicial()
    assert gestor.jugador_inicial == jugadores[1]

def test_flujo_turnos_sentido_horario():
    jugadores = [JugadorBot("cecilia"), JugadorBot("geoffrey"), JugadorBot("julio"), JugadorBot("hugo")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[1]
    gestor.definir_sentido("horario")

    orden = gestor.obtener_orden_turnos()
    assert orden == [jugadores[1], jugadores[2], jugadores[3], jugadores[0]]

def test_flujo_turnos_sentido_antihorario():
    jugadores = [JugadorBot("cecilia"), JugadorBot("geoffrey"), JugadorBot("julio"), JugadorBot("hugo")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[2]
    gestor.definir_sentido("antihorario")

    orden = gestor.obtener_orden_turnos()
    assert orden == [jugadores[2], jugadores[1], jugadores[0], jugadores[3]]

def test_partida_terminada():
    jugador1 = JugadorBot("geoffrey")
    jugador2 = JugadorBot("julio")
    jugador3 = JugadorBot("hugo")

    while jugador2.cacho.numero_dados() > 0:
        jugador2.cacho.quitar_dado()
    while jugador3.cacho.numero_dados() > 0:
        jugador3.cacho.quitar_dado()

    gestor = GestorPartida([jugador1, jugador2, jugador3])
    assert gestor.partida_terminada() is True
    

def test_iniciar_partida_con_bots():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)

    gestor.iniciar_partida()

    assert gestor.jugador_inicial in jugadores
    assert gestor.sentido in ["horario", "antihorario"]



def test_iniciar_ronda_sin_jugador_inicial():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio")]
    gestor = GestorPartida(jugadores)

    with pytest.raises(ValueError, match="Debe determinarse el jugador inicial antes de iniciar la partida"):
        gestor.iniciar_ronda()
        
        
def test_iniciar_partida_con_un_solo_jugador_invalido():
    jugador = JugadorBot("hugo")
    gestor = GestorPartida([jugador])

    with pytest.raises(ValueError, match="Se requieren al menos 2 jugadores para iniciar la partida"):
        gestor.iniciar_partida()
        

def test_partida():
    jugadores = [JugadorBot("Hugo"), JugadorBot("Julio"), JugadorBot("Geoffrey")]
    gestor = GestorPartida(jugadores)
    gestor.iniciar_partida()

    activos = [j for j in gestor.jugadores if j.cacho.numero_dados() > 0]
    assert len(activos) == 1


def test_jugar_ronda_apuesta_inicial():
    jugadores = [JugadorBot("Hugo"), JugadorBot("Julio")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[0]
    gestor.definir_sentido("horario")
    gestor.iniciar_ronda()

    gestor.jugar_ronda() #se debe fijar una apuesta

    assert gestor.apuesta_actual is not None
    assert isinstance(gestor.apuesta_actual, Apuesta)
    assert gestor.apuesta_actual.jugador_que_aposto in jugadores


def test_jugar_ronda_duda_y_pierde():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[0]
    gestor.definir_sentido("horario")
    gestor.iniciar_ronda()

    #forzar apuesta alta para que el bot que duda pierda
    gestor.apuesta_actual = Apuesta(cantidad=5, pinta="As", jugador_que_aposto=jugadores[0])
    gestor.turno_index = 1  # Julio duda

    gestor.jugar_ronda()

    assert jugadores[1].cacho.numero_dados() < 5 or jugadores[0].cacho.numero_dados() < 5
    assert gestor.jugador_afectado in jugadores
    
def test_jugar_ronda_calzar_valido(monkeypatch):
    jugadores = [JugadorBot("hugo"), JugadorBot("julio")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[0]
    gestor.definir_sentido("horario")
    gestor.iniciar_ronda()

    pinta = jugadores[1].cacho.dados[0].pinta()
    apuesta = Apuesta(cantidad=5, pinta=pinta, jugador_que_aposto=jugadores[0])
    assert ValidadorApuesta.es_valida(apuesta, None, jugadores[1])

    gestor.apuesta_actual = apuesta
    gestor.turno_index = 1

    monkeypatch.setattr(JugadorBot, "elegir_accion", lambda self, apuesta: {"tipo": "calzar"})

    gestor.jugar_ronda(apuesta_inicial_tests=gestor.apuesta_actual)

    assert gestor.jugador_afectado == jugadores[1]


def test_jugar_ronda_calzar_falla(monkeypatch):
    jugadores = [JugadorBot("hugo"), JugadorBot("julio")]
    gestor = GestorPartida(jugadores)
    gestor.jugador_inicial = jugadores[0]
    gestor.definir_sentido("horario")
    gestor.iniciar_ronda()

    #forzar apuesta que no se puede calzar
    gestor.apuesta_actual = Apuesta(cantidad=5, pinta="Tres", jugador_que_aposto=jugadores[0])
    gestor.turno_index = 1  # Julio calza

    monkeypatch.setattr(JugadorBot, "elegir_accion", lambda self, apuesta: {"tipo": "calzar"})

    gestor.jugar_ronda(apuesta_inicial_tests=gestor.apuesta_actual)

    assert jugadores[1].cacho.numero_dados() < 5
    assert gestor.jugador_afectado == jugadores[1]


def test_activar_ronda_obligada():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)

    jugadores[0].cacho.dados = [Dado()]
    jugadores[0].cacho.dado1.valor = 1

    gestor.pedir_modo_obligado = lambda j: "cerrado"
    gestor.iniciar_ronda()

    assert jugadores[0].ronda_obligada is True
    assert jugadores[0].obligado_activado is True
    assert jugadores[0].modo_obligado == "cerrado"

    # demás no están obligados
    assert not jugadores[1].ronda_obligada
    assert not jugadores[2].ronda_obligada


def test_no_reactivar_ronda_obligada_en_segunda_vez():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)

    jugadores[1].obligado_activado = True
    jugadores[1].ronda_obligada = False
    jugadores[1].modo_obligado = "cerrado"

    jugadores[1].cacho.dados = [Dado()]
    jugadores[1].cacho.dado1.valor = 2  # Tonto

    # demás tienen más de un dado
    jugadores[0].cacho.dados = [Dado() for _ in range(3)]
    jugadores[2].cacho.dados = [Dado() for _ in range(5)]

    gestor.pedir_modo_obligado = lambda j: "abierto"  # no debería llamarse

    gestor.iniciar_ronda()

    assert jugadores[1].ronda_obligada is False
    assert jugadores[1].modo_obligado == "cerrado"  # se mantiene el anterior


def test_contador_sin_comodines_en_obligado():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio")]
    jugadores[0].cacho.dados = [Dado(), Dado()]
    jugadores[0].cacho.dados[0].valor = 1  # As
    jugadores[0].cacho.dados[1].valor = 2 

    contador = Contador_pintas(jugadores[0].cacho)
    total = contador.contar_pintas("Tonto", obligar=True)

    assert total == 1 # el as no debe contar como comodín


def test_activar_ronda_obligada_invalido():
    jugadores = [JugadorBot("hugo"), JugadorBot("julio"), JugadorBot("geoffrey")]
    gestor = GestorPartida(jugadores)

    #jlio tiene 2 dados y nunca ha activado ronda obligada
    jugadores[1].obligado_activado = False
    jugadores[1].ronda_obligada = False
    jugadores[1].cacho.dados = [Dado(), Dado()]
    jugadores[1].cacho.dados[0].valor = 2
    jugadores[1].cacho.dados[1].valor = 5

    jugadores[0].cacho.dados = [Dado() for _ in range(5)]
    jugadores[2].cacho.dados = [Dado() for _ in range(4)]

    gestor.pedir_modo_obligado = lambda j: "cerrado"  # no debería llamarse

    gestor.iniciar_ronda()

    assert jugadores[1].ronda_obligada is False
    assert jugadores[1].obligado_activado is False
    assert gestor.ronda_obligada is False or gestor.jugador_obligado != jugadores[1]
