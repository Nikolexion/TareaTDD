from src.servicios.generador_aleatorio import GeneradorAleatorio

def test_aleatorio_entre_1_y_6_sin_mock():
    generador = GeneradorAleatorio()
    for _ in range(100):
        valor = generador.generador_aleatorio()
        assert 1<=valor<=6

def test_sin_inyección_con_randint(mocker):
    randint_mock = mocker.patch("src.servicios.generador_aleatorio.random.randint",return_value=5)

    gen = GeneradorAleatorio()
    assert gen.generador_aleatorio() == 5
    #el mock se llamó con argumento entre 1 a 6
    randint_mock.assert_called_once_with(1, 6)


def test_con_inyección(mocker):
    randint_mock = mocker.patch("src.servicios.generador_aleatorio.random.randint")

    gen = GeneradorAleatorio(generador_aleatorio=lambda: 3)
    assert gen.generador_aleatorio() == 3
    #verifica que no se llamó random.randint
    randint_mock.assert_not_called()