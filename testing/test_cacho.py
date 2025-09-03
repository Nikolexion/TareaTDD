from src.juego.cacho import Cacho

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
    assert cacho.numero_dados_en_juego() == 5

def test_quitar_dado_con_mas_de_cinco():
    """Prueba quitar dado cuando se tienen más de 5 dados virtuales"""
    cacho = Cacho()
    
    # Agregar dados extra para simular más de 5
    cacho.sumar_dado()
    cacho.sumar_dado()
    inicial = cacho.num_dados
    assert inicial > 5
    
    # Quitar dado cuando num_dados > 5
    cacho.quitar_dado()
    assert cacho.num_dados == inicial - 1
    assert len(cacho.dados) == 5  # Los dados físicos no cambian