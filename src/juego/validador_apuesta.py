import math
from src.juego.dado import Dado

#clase con métodos estáticos, sin estados
class ValidadorApuesta:

    @staticmethod
    def es_valida(nueva_apuesta, apuesta_anterior, jugador):
        pinta_actual = nueva_apuesta.pinta
        cantidad_actual = nueva_apuesta.cantidad
        num_dados = jugador.cacho.numero_dados()

        #si es que es la primera apuesta
        if apuesta_anterior is None:
            return ValidadorApuesta._validar_apuesta_inicial(pinta_actual, num_dados)

        pinta_anterior = apuesta_anterior.pinta
        cantidad_anterior = apuesta_anterior.cantidad

        # cambio a ases
        if pinta_actual == "As" and pinta_anterior != "As":
            cantidad_convertida = ValidadorApuesta._convertir_a_ases(cantidad_anterior)
            return cantidad_actual >= cantidad_convertida

        # cambio desdde ases
        if pinta_anterior == "As" and pinta_actual != "As":
            cantidad_convertida = ValidadorApuesta._convertir_desde_ases(cantidad_anterior)
            return cantidad_actual >= cantidad_convertida

        # apuesta caso normal
        return (cantidad_actual > cantidad_anterior) or (
            cantidad_actual == cantidad_anterior and
            ValidadorApuesta._pinta_mayor(pinta_actual, pinta_anterior)
        )

    @staticmethod
    def _validar_apuesta_inicial(pinta, num_dados):
        if pinta == "As" and num_dados > 1:
            return False
        return True

    @staticmethod
    def _convertir_a_ases(cantidad):
        if cantidad % 2 == 0: #caso que sea par: cantidad/2 +1
            return cantidad // 2 + 1
        else:
            return math.ceil(cantidad / 2) #caso impar: redondear hacia arriba

    @staticmethod
    def _convertir_desde_ases(cantidad):
        # cantidad * 2 + 1
        return cantidad * 2 + 1

    @staticmethod
    def _pinta_mayor(pinta_nueva, pinta_anterior):
        pinta_inversa = {v: k for k, v in Dado.PINTA.items()}
        return pinta_inversa[pinta_nueva] > pinta_inversa[pinta_anterior]
