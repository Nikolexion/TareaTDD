import pytest

from src.juego.arbitro_ronda import ArbitroRonda, Apuesta
from src.juego.cacho import Cacho
from src.juego.dado import Dado

    
def test_resultado_duda_si_supera_apuesta(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 3, 1, 5, 2, 2, 2, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = mocker.Mock()
    jugador_apuesta.cacho = Cacho()
    jugador_duda = mocker.Mock()
    jugador_duda.cacho = Cacho()

    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador_apuesta)
    arbitro = ArbitroRonda(jugador_apuesta, [jugador_apuesta, jugador_duda])

    resultado = arbitro.resolver_duda(apuesta, jugador_duda.cacho, jugador_duda)
    assert resultado.pierde_dado == jugador_duda


def test_resultado_duda_no_cumple_apuesta(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 2, 2, 2, 4, 4, 5, 4, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = mocker.Mock()
    jugador_apuesta.cacho = Cacho()
    jugador_duda = mocker.Mock()
    jugador_duda.cacho = Cacho()
    
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador_apuesta)
    arbitro = ArbitroRonda(jugador_apuesta, [jugador_apuesta, jugador_duda])

    resultado = arbitro.resolver_duda(apuesta, jugador_duda.cacho, jugador_duda)
    assert resultado.pierde_dado == jugador_apuesta
    

def test_resolver_calzar_bueno(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 1, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador1 = mocker.Mock()
    jugador_calza = mocker.Mock()
    jugador1.num_dados = 2
    jugador_calza.num_dados = 2

    arbitro = ArbitroRonda(0, [jugador1, jugador_calza])
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=jugador1)
    cacho = Cacho()

    resultado = arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador_calza)
    assert resultado.acierta is True
    assert resultado.recupera_jugador == jugador_calza
    assert resultado.pierden_dado == []


def test_calzar_incorrecto_pierde_quien_calza(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 2, 1, 2, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador1 = mocker.Mock()
    jugador_calza = mocker.Mock()
    jugador1.num_dados = 3
    jugador_calza.num_dados = 3
    arbitro = ArbitroRonda(0, [jugador1, jugador_calza])
    apuesta = Apuesta(cantidad=3, pinta=3, jugador_que_aposto=1)
    cacho = Cacho()

    resultado = arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador_calza)
    assert resultado.acierta is False
    assert resultado.pierden_dado == [jugador_calza]


def test_puede_calzar_mitad_o_mas(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 3, 3, 6]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = mocker.Mock()
    jugador_calza = mocker.Mock()
    jugador_apuesta.num_dados = 3
    jugador_calza.num_dados = 3

    arbitro = ArbitroRonda(0, [jugador_apuesta, jugador_calza])
    apuesta = Apuesta(cantidad=4, pinta=3, jugador_que_aposto=jugador_apuesta)
    cacho = Cacho()

    resultado = arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador_calza)
    assert resultado.acierta is True
    assert resultado.recupera_jugador is jugador_calza
    assert resultado.pierden_dado == []


def test_calzar_por_un_dado(mocker):
    mock_generador = mocker.Mock()
    mock_generador.generar.side_effect = [3, 3, 3, 1, 2]
    mocker.patch("src.juego.dado.GeneradorAleatorio", return_value=mock_generador)

    jugador_apuesta = mocker.Mock()
    jugador_calza = mocker.Mock()
    jugador_apuesta.num_dados = 5
    jugador_calza.num_dados = 1

    arbitro = ArbitroRonda(0, [jugador_apuesta, jugador_calza])
    apuesta = Apuesta(cantidad=4, pinta=3, jugador_que_aposto=jugador_apuesta)
    cacho = Cacho()

    resultado = arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador_calza)
    assert resultado.acierta is True
    assert resultado.recupera_jugador is jugador_calza
    assert resultado.pierden_dado == []


def test_no_puede_calzar(mocker):
    jugador_apuesta = mocker.Mock()
    jugador_calza = mocker.Mock()
    jugador_apuesta.num_dados = 3
    jugador_calza.num_dados = 3

    arbitro = ArbitroRonda(0, [jugador_apuesta, jugador_calza])
    apuesta = Apuesta(cantidad=2, pinta=3, jugador_que_aposto=jugador_apuesta)

    cacho = Cacho()

    with pytest.raises(ValueError):
        arbitro.resolver_calzar(apuesta, cacho, jugador_calza=jugador_calza)


def test_pinta_en_string_con_int_devuelve_nombre():
    arbitro = ArbitroRonda(0, [])
    assert arbitro.pinta_en_string(Apuesta(cantidad=1, pinta=3)) == Dado.PINTA[3]


def test_pinta_en_string_con_string_lo_deja_igual():
    arbitro = ArbitroRonda(0, [])
    assert arbitro.pinta_en_string(Apuesta(cantidad=1, pinta="Tren")) == "Tren"


def test_puede_calzar_falla_si_cantidad_invalida(mocker):
    j1 = mocker.Mock(num_dados=1)
    j2 = mocker.Mock(num_dados=1)
    arbitro = ArbitroRonda(0, [j1, j2])
    with pytest.raises(ValueError):
        arbitro.puede_calzar(Apuesta(cantidad=0, pinta=3, jugador_que_aposto=j1), j2)


def test_puede_calzar_falla_si_jugador_con_dados_negativos(mocker):
    j1 = mocker.Mock(num_dados=-1)
    j2 = mocker.Mock(num_dados=1)
    arbitro = ArbitroRonda(0, [j1, j2])
    with pytest.raises(ValueError):
        arbitro.puede_calzar(Apuesta(cantidad=1, pinta=3, jugador_que_aposto=j1), j2)


def test_puede_calzar_falla_si_total_dados_en_juego_es_cero(mocker):
    j1 = mocker.Mock(num_dados=0)
    j2 = mocker.Mock(num_dados=0)
    arbitro = ArbitroRonda(0, [j1, j2])
    with pytest.raises(ValueError):
        arbitro.puede_calzar(Apuesta(cantidad=1, pinta=3, jugador_que_aposto=j1), j2)


def test_puede_calzar_falla_si_calzador_tiene_cero_dados(mocker):
    j1 = mocker.Mock(num_dados=2)
    j2 = mocker.Mock(num_dados=0)
    arbitro = ArbitroRonda(0, [j1, j2])
    with pytest.raises(ValueError):
        arbitro.puede_calzar(Apuesta(cantidad=1, pinta=3, jugador_que_aposto=j1), j2)


def test_puede_calzar_lee_num_dados_de_cacho_para_jugador_de_la_lista(mocker):
    cacho_j1 = mocker.Mock()
    cacho_j1.numero_dados.return_value = 2
    j1 = mocker.Mock()
    if hasattr(j1, "num_dados"):
        del j1.num_dados
    j1.cacho = cacho_j1
    j2 = mocker.Mock(num_dados=1)
    arbitro = ArbitroRonda(0, [j1, j2])
    assert arbitro.puede_calzar(Apuesta(cantidad=2, pinta=3, jugador_que_aposto=j1), j2) is True


def test_puede_calzar_lee_num_dados_de_cacho_para_calzador_y_true_por_un_dado(mocker):
    j1 = mocker.Mock(num_dados=2)
    cacho_j2 = mocker.Mock()
    cacho_j2.numero_dados.return_value = 1
    j2 = mocker.Mock()
    if hasattr(j2, "num_dados"):
        del j2.num_dados
    j2.cacho = cacho_j2
    arbitro = ArbitroRonda(0, [j1, j2])
    assert arbitro.puede_calzar(Apuesta(cantidad=1, pinta=3, jugador_que_aposto=j1), j2) is True


def test_puede_calzar_falla_si_jugador_sin_num_dados_ni_cacho(mocker):
    j1 = mocker.Mock()
    if hasattr(j1, "num_dados"):
        del j1.num_dados
    if hasattr(j1, "cacho"):
        del j1.cacho

    j2 = mocker.Mock(num_dados=1)
    arbitro = ArbitroRonda(0, [j1, j2])

    with pytest.raises(ValueError):
        arbitro.puede_calzar(Apuesta(cantidad=1, pinta=3, jugador_que_aposto=j1), j2)