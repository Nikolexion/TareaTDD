from src.juego.arbitro_ronda import ArbitroRonda, Apuesta
from src.juego.cacho import Cacho


def test_resultado_duda_si_supera_apuesta(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 3, 1, 5]  # caras controladas
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)
    cacho = Cacho()
    apuesta = Apuesta(cantidad=3, pinta=3)
    arbitro = ArbitroRonda(0, [object(), object()])
    resultado = arbitro.resolver_duda(apuesta, cacho, player_duda="2", player_apuesta="1")
    assert resultado.pierde_dado == "2"

def test_resultado_duda_no_cumple_apuesta(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 2, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    cacho = Cacho()
    apuesta = Apuesta(cantidad=3, pinta=3)
    arbitro = ArbitroRonda(0, [object(), object()])
    resultado = arbitro.resolver_duda(apuesta, cacho, player_duda="2", player_apuesta="1")
    assert resultado.pierde_dado == "1"