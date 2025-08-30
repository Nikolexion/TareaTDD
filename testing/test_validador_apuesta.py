import pytest

from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.arbitro_ronda import Apuesta
from src.juego.jugador import Jugador

def test_apuesta_mayor_cantidad_valida():
    jugador = Jugador()
    anterior = Apuesta(cantidad=3, pinta="Cuadra")
    nueva = Apuesta(cantidad=4, pinta="Cuadra")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_pinta_superior_valida():
    jugador = Jugador()
    anterior = Apuesta(cantidad=3, pinta="Cuadra")
    nueva = Apuesta(cantidad=3, pinta="Quina")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_menor_cantidad_invalida():
    jugador = Jugador()
    anterior = Apuesta(cantidad=3, pinta="Cuadra")
    nueva = Apuesta(cantidad=2, pinta="Cuadra")
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)
    
def test_apuesta_pinta_menor_invalida():
    jugador = Jugador()
    anterior = Apuesta(cantidad=3, pinta="Quina")
    nueva = Apuesta(cantidad=3, pinta="Tren")
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_par_valido():
    jugador = Jugador()
    anterior = Apuesta(cantidad=4, pinta="Cuadra")
    nueva = Apuesta(cantidad=3, pinta="As")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_impar_valido():
    jugador = Jugador()
    anterior = Apuesta(cantidad=5, pinta="Quina")
    nueva = Apuesta(cantidad=3, pinta="As")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)
    
def test_cambio_a_ases_par_invalido():
    jugador = Jugador()
    anterior = Apuesta(cantidad=4, pinta="Cuadra") 
    nueva = Apuesta(cantidad=2, pinta="As")        
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_impar_invalido():
    jugador = Jugador()
    anterior = Apuesta(cantidad=5, pinta="Quina") 
    nueva = Apuesta(cantidad=2, pinta="As") 
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)
    
def test_cambio_desde_ases_valido():
    jugador = Jugador()
    anterior = Apuesta(cantidad=2, pinta="As")
    nueva = Apuesta(cantidad=5, pinta="Cuadra")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_desde_ases_invalido():
    jugador = Jugador()
    anterior = Apuesta(cantidad=2, pinta="As")
    nueva = Apuesta(cantidad=4, pinta="Cuadra")
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_inicial_con_ases_invalida():
    jugador = Jugador()
    apuesta_nueva = Apuesta(cantidad=2, pinta="As")
    assert not ValidadorApuesta.es_valida(apuesta_nueva, None, jugador)

def test_apuesta_inicial_con_ases_valida():
    jugador = Jugador()
    jugador.cacho.dados = jugador.cacho.dados[:1]
    jugador.cacho.num_dados = 1
    apuesta_nueva = Apuesta(cantidad=1, pinta="As")
    assert ValidadorApuesta.es_valida(apuesta_nueva, None, jugador)
