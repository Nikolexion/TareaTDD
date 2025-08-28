from juego.contador_pintas import Contador_pintas
from juego.cacho import Cacho

def test_contador_pintas():
    cacho = Cacho()
    contador = Contador_pintas(False, cacho)
    assert contador.contar_pintas() is not None
