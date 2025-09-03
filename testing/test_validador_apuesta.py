import pytest

from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.arbitro_ronda import Apuesta
from src.juego.jugador import JugadorBot

def test_apuesta_mayor_cantidad_valida():
    """
    Verifica que una apuesta con mayor cantidad que la anterior sea válida.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=3, pinta="Cuadra")
    nueva = Apuesta(cantidad=4, pinta="Cuadra")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_pinta_superior_valida():
    """
    Verifica que una apuesta con misma cantidad pero pinta superior sea válida.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=3, pinta="Cuadra")
    nueva = Apuesta(cantidad=3, pinta="Quina")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_menor_cantidad_invalida():
    """
    Verifica que una apuesta con menor cantidad que la anterior sea inválida.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=3, pinta="Cuadra")
    nueva = Apuesta(cantidad=2, pinta="Cuadra")
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_pinta_menor_invalida():
    """
    Verifica que una apuesta con misma cantidad pero pinta inferior sea inválida.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=3, pinta="Quina")
    nueva = Apuesta(cantidad=3, pinta="Tren")
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_par_valido():
    """
    Verifica que una apuesta con Ases sea válida si supera la conversión desde cantidad par.
    Ejemplo: 4 Cuadra → mínimo 3 Ases.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=4, pinta="Cuadra")
    nueva = Apuesta(cantidad=3, pinta="As")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_impar_valido():
    """
    Verifica que una apuesta con Ases sea válida si supera la conversión desde cantidad impar.
    Ejemplo: 5 Quina → mínimo 3 Ases.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=5, pinta="Quina")
    nueva = Apuesta(cantidad=3, pinta="As")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_par_invalido():
    """
    Verifica que una apuesta con Ases sea inválida si no supera la conversión desde cantidad par.
    Ejemplo: 4 Cuadra → mínimo 3 Ases → 2 Ases es inválido.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=4, pinta="Cuadra") 
    nueva = Apuesta(cantidad=2, pinta="As")        
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_a_ases_impar_invalido():
    """
    Verifica que una apuesta con Ases sea inválida si no supera la conversión desde cantidad impar.
    Ejemplo: 5 Quina → mínimo 3 Ases → 2 Ases es inválido.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=5, pinta="Quina") 
    nueva = Apuesta(cantidad=2, pinta="As") 
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_desde_ases_valido():
    """
    Verifica que una apuesta desde Ases sea válida si supera la conversión.
    Ejemplo: 2 Ases → mínimo 5 Cuadra.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=2, pinta="As")
    nueva = Apuesta(cantidad=5, pinta="Cuadra")
    assert ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_cambio_desde_ases_invalido():
    """
    Verifica que una apuesta desde Ases sea inválida si no supera la conversión.
    Ejemplo: 2 Ases → mínimo 5 Cuadra → 4 Cuadra es inválido.
    """
    jugador = JugadorBot("geoffrey")
    anterior = Apuesta(cantidad=2, pinta="As")
    nueva = Apuesta(cantidad=4, pinta="Cuadra")
    assert not ValidadorApuesta.es_valida(nueva, anterior, jugador)

def test_apuesta_inicial_con_ases_invalida():
    """
    Verifica que una apuesta inicial con Ases sea inválida si el jugador tiene más de 1 dado.
    """
    jugador = JugadorBot("geoffrey")
    apuesta_nueva = Apuesta(cantidad=2, pinta="As")
    assert not ValidadorApuesta.es_valida(apuesta_nueva, None, jugador)

def test_apuesta_inicial_con_ases_valida():
    """
    Verifica que una apuesta inicial con Ases sea válida si el jugador tiene solo 1 dado.
    """
    jugador = JugadorBot("geoffrey")
    jugador.cacho.dados = jugador.cacho.dados[:1]
    jugador.cacho.num_dados = 1
    apuesta_nueva = Apuesta(cantidad=1, pinta="As")
    assert ValidadorApuesta.es_valida(apuesta_nueva, None, jugador)
