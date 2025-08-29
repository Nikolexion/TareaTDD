from src.juego.arbitro_ronda import ArbitroRonda, Apuesta

#Si duda
def test_resultado_duda_si_supera_apuesta():
    #suponemos caras
    caras_mesa = [1, 3, 3, 3]
    #suponemos apuesta
    apuesta = Apuesta(cantidad = 3, pinta=3)
    #instancia de arbitro
    arbitro = ArbitroRonda(0, [object(), object()])
    #resultado duda
    resultado = arbitro.resolver_duda(apuesta, caras_mesa, player_duda = "2", player_apuesta = "1")
    assert resultado.pierde_dado == "2"


def test_resultado_duda_no_cumple_apuesta():
    caras_mesa = [3, 3]
    apuesta = Apuesta(cantidad=3, pinta=3)
    arbitro = ArbitroRonda(0, [object(), object()])
    resultado = arbitro.resolver_duda(apuesta, caras_mesa, player_duda="2", player_apuesta="1")
    assert resultado.pierde_dado == "1"
