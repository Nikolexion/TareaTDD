from juego.contador_pintas import Contador_pintas
from juego.cacho import Cacho

def test_contador_pintas():
    cacho = Cacho()
    contador = Contador_pintas(cacho)
    assert contador.contar_pintas("Tonto", False) is not None
