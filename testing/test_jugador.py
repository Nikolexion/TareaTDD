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


def test_elegir_accion_humano(monkeypatch):
    inputs = iter(["apostar", "2", "Tren"]) #se simula un input de apostar 2
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    jugador = JugadorHumano("Antonia")
    accion = jugador.elegir_accion(apuesta_actual=None)

    assert accion["tipo"] == "apostar"
    assert isinstance(accion["apuesta"], Apuesta)
    assert accion["apuesta"].cantidad == 2
    assert accion["apuesta"].pinta == "Tren"
    assert accion["apuesta"].jugador_que_aposto == jugador