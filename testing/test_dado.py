from juego.dado import Dado

def test_dado():
    dado = Dado()

    for _ in range(100):
        resultado = dado.lanzar()
        assert 1 <= resultado <= 6