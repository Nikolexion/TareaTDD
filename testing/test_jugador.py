from src.juego.cacho import Cacho
from src.juego.dado import Dado
from src.juego.jugador import Jugador

#Crear jugador con 5 dados
def test_inicializar_jugador():
    jugador = Jugador()
    assert isinstance(jugador.cacho, Cacho)
    assert len(jugador.cacho.dados) == 5
