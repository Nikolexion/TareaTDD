from src.juego.cacho import Cacho
from src.juego.dado import Dado
from src.juego.jugador import JugadorBot, JugadorHumano
from src.juego.arbitro_ronda import Apuesta

def test_inicializar_jugador_bot():
    """
    Verifica que un JugadorBot se inicializa correctamente:
    - Tiene un cacho con 5 dados.
    - Su nombre se asigna correctamente.
    """
    jugador = JugadorBot("geoffrey")
    assert isinstance(jugador.cacho, Cacho)
    assert len(jugador.cacho.dados) == 5
    assert jugador.nombre == "geoffrey"

def test_elegir_sentido_juego_bot():
    """
    Verifica que el bot elige un sentido de juego válido ('horario' o 'antihorario').
    """
    jugador = JugadorBot("geoffrey")
    sentido = jugador.elegir_sentido()
    assert sentido in ["horario", "antihorario"]

def test_elegir_accion_bot():
    """
    Verifica que el bot elige una acción válida al iniciar la ronda:
    - Debe apostar si no hay apuesta previa.
    - La acción debe ser un diccionario con tipo 'apostar' y una instancia de Apuesta.
    """
    jugador = JugadorBot("geoffrey")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert isinstance(accion, dict)
    assert accion["tipo"] == "apostar"
    assert isinstance(accion["apuesta"], Apuesta)
    assert accion["apuesta"].jugador_que_aposto == jugador

def test_elegir_accion_humano_apostar(monkeypatch):
    """
    Simula que un jugador humano elige 'apostar' con cantidad 2 y pinta 'Tren'.
    Verifica que la acción se construye correctamente.
    """
    inputs = iter(["apostar", "2", "Tren"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("Antonia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "apostar"
    assert isinstance(accion["apuesta"], Apuesta)
    assert accion["apuesta"].cantidad == 2
    assert accion["apuesta"].pinta == "Tren"
    assert accion["apuesta"].jugador_que_aposto == jugador

def test_elegir_accion_humano_dudar(monkeypatch):
    """
    Simula que un jugador humano elige 'dudar'.
    Verifica que la acción se interpreta correctamente.
    """
    inputs = iter(["dudar"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("cecilia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "dudar"

def test_elegir_accion_humano_calzar(monkeypatch):
    """
    Simula que un jugador humano elige 'calzar'.
    Verifica que la acción se interpreta correctamente.
    """
    inputs = iter(["calzar"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("cecilia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "calzar"

def test_elegir_sentido_juego_humano(monkeypatch):
    """
    Simula que un jugador humano elige el sentido 'antihorario'.
    Verifica que se interpreta correctamente.
    """
    inputs = iter(["antihorario"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("cecilia")
    sentido = jugador.elegir_sentido()

    assert sentido == "antihorario"
