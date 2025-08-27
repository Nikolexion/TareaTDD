from juego.cacho import Cacho

def test_agitar_cacho():
    cacho = Cacho()
    resultado = cacho.agitar()
    assert resultado is not None

def test_numero_dados_cacho():
    cacho = Cacho()
    assert cacho.numero_dados() == 5