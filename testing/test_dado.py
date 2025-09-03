from src.juego.dado import Dado
from src.servicios.generador_aleatorio import GeneradorAleatorio

def test_lanzar_dado():
    dado = Dado()

    for _ in range(100):
        resultado = dado.lanzar()
        assert 1 <= resultado <= 6

def test_pinta_dado():
    dado = Dado()
    dado.valor = 3
    assert dado.pinta() == "Tren"
    
def test_dado_con_funcion_generadora():
    def generador_mock():
        return 4

    dado = Dado(generador=generador_mock)
    valor = dado.lanzar()

    assert valor == 4
    assert dado.pinta() == "Cuadra"


def test_dado_con_generador_aleatorio_directo():
    # Generador que siempre devuelve 6 (Sexto)
    generador_fijo = GeneradorAleatorio(lambda: 6)

    dado = Dado(generador=generador_fijo)
    valor = dado.lanzar()

    assert valor == 6
    assert dado.pinta() == "Sexto"
