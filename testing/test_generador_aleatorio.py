from src.servicios.generador_aleatorio import GeneradorAleatorio

def test_aleatorio_entre_1_y_6_sin_mock():
    generador = GeneradorAleatorio()
    for _ in range(100):
        valor = generador.generador_aleatorio()
        assert 1<=valor<=6

def test_sin_inyección_con_randint(mocker):
    randint_mock = mocker.patch("src.servicios.generador_aleatorio.random.randint",return_value=5)

    genenerador = GeneradorAleatorio()
    assert genenerador.generador_aleatorio() == 5
    randint_mock.assert_called_once_with(1, 6)


def test_con_inyección(mocker):
    randint_mock = mocker.patch("src.servicios.generador_aleatorio.random.randint")

    generador = GeneradorAleatorio(generador_aleatorio=lambda: 3)
    assert generador.generador_aleatorio() == 3
    randint_mock.assert_not_called()