from juego.cacho import Cacho

def test_agitar_cacho():
    cacho = Cacho()
    resultado = cacho.agitar()
    assert resultado is not None

def test_numero_dados_cacho():
    cacho = Cacho()
    assert cacho.numero_dados() == 5

def test_quitar_dado_cacho():
    cacho = Cacho()
    cacho.quitar_dado()
    assert cacho.numero_dados() == 4

def test_sumar_dado_cacho():
    cacho = Cacho()
    cacho.quitar_dado()
    cacho.sumar_dado()
    assert cacho.numero_dados() == 5

def test_sumar_sexto_dado_cacho():
    cacho = Cacho()
    cacho.sumar_dado()
    assert cacho.numero_dados() == 5