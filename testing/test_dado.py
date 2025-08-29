from src.juego.dado import Dado

def test_lanzar_dado():
    dado = Dado()

    for _ in range(100):
        resultado = dado.lanzar()
        assert 1 <= resultado <= 6

def test_pinta_dado():
    dado = Dado()
    dado.valor = 3
    assert dado.pinta() == "Tren"
    