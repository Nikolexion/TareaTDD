from juego.cacho import Cacho

def test_agitar_cacho():
    cacho = Cacho()
    resultado = cacho.agitar()
    assert resultado is not None