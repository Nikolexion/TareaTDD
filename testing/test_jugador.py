from src.juego.cacho import Cacho
from src.juego.dado import Dado
from src.juego.jugador import JugadorBot, JugadorHumano

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
    


