from src.juego.cacho import Cacho
from src.juego.dado import Dado
from src.juego.jugador import JugadorBot, JugadorHumano
from src.juego.arbitro_ronda import Apuesta

#Crear jugador con 5 dados
def test_inicializar_jugador_bot():
    jugador = JugadorBot("geoffrey")
    assert isinstance(jugador.cacho, Cacho)
    assert len(jugador.cacho.dados) == 5
    assert jugador.nombre == "geoffrey"
    
def test_elegir_sentido_juego_bot():
    jugador = JugadorBot("geoffrey")
    sentido = jugador.elegir_sentido()
    assert sentido in ["horario", "antihorario"]


def test_elegir_accion_bot():
    jugador = JugadorBot("geoffrey")
    accion = jugador.elegir_accion(apuesta_actual=None) #suponiendo primera apuesta

    #diccionario con tipo de jugada, pinta, cantidad
    assert isinstance(accion, dict)
    assert accion["tipo"] == "apostar"
    assert isinstance(accion["apuesta"], Apuesta)
    assert accion["apuesta"].jugador_que_aposto == jugador


def test_elegir_accion_humano_apostar(monkeypatch):
    inputs = iter(["apostar", "2", "Tren"]) #se simula un input de apostar 2 trenes
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("Antonia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "apostar"
    assert isinstance(accion["apuesta"], Apuesta)
    assert accion["apuesta"].cantidad == 2
    assert accion["apuesta"].pinta == "Tren"
    assert accion["apuesta"].jugador_que_aposto == jugador
    
def test_elegir_accion_humano_dudar(monkeypatch):
    inputs = iter(["dudar"]) #se simula un input de apostar 2 trenes
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("cecilia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "dudar"


def test_elegir_accion_humano_calzar(monkeypatch):
    inputs = iter(["calzar"]) #se simula un input de apostar 2 trenes
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("cecilia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "calzar"


def test_elegir_sentido_juego_humano(monkeypatch):
    inputs = iter(["antihorario"]) #se simula un input de apostar 2 trenes
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("cecilia")
    sentido = jugador.elegir_sentido()

    assert sentido == "antihorario"
    