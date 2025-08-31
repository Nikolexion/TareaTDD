from src.juego.arbitro_ronda import ArbitroRonda, Apuesta
from src.juego.cacho import Cacho


def test_resultado_duda_si_supera_apuesta(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 3, 1, 5]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = "1"
    jugador_duda = "2"

    cacho = Cacho()
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador_apuesta)
    arbitro = ArbitroRonda(0, [object(), object()])

    resultado = arbitro.resolver_duda(apuesta, cacho, jugador_duda=jugador_duda)
    assert resultado.pierde_dado == jugador_duda


def test_resultado_duda_no_cumple_apuesta(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 2, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = "1"
    jugador_duda = "2"

    cacho = Cacho()
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador_apuesta)
    arbitro = ArbitroRonda(0, [object(), object()])

    resultado = arbitro.resolver_duda(apuesta, cacho, jugador_duda=jugador_duda)
    assert resultado.pierde_dado == jugador_apuesta


def test_resolver_calzar_bueno(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 1, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador1 = mocker.Mock()
    jugador2 = mocker.Mock()
    jugador1.num_dados = 2
    jugador2.num_dados = 2

    arbitro = ArbitroRonda(0, [jugador1, jugador2])
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador1)
    cacho = Cacho()

    resultado = arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador2)
    assert resultado.acierta is True
    assert resultado.pierden_dado == [jugador1]

def test_calzar_incorrecto_pierde_quien_calza(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 2 , 1, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = mocker.Mock()
    jugador_calza = mocker.Mock()

    arbitro = ArbitroRonda(0, [jugador_apuesta, jugador_calza])
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador_apuesta)
    cacho = Cacho()

    resultado = arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador_calza)

    assert resultado.acierta is False
    assert resultado.pierden_dado == [jugador_calza]
