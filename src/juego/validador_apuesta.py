import math
from src.juego.dado import Dado

class ValidadorApuesta:
    """
    Clase utilitaria con métodos estáticos para validar apuestas en el juego.
    No mantiene estado interno. Se encarga de verificar si una nueva apuesta
    supera correctamente la anterior, considerando reglas especiales como el uso de Ases.
    """

    @staticmethod
    def es_valida(nueva_apuesta, apuesta_anterior, jugador):
        """
        Determina si una nueva apuesta es válida en relación a la apuesta anterior.

        Reglas:
        - Si no hay apuesta anterior, se valida con _validar_apuesta_inicial.
        - Si hay cambio hacia o desde "As", se aplica conversión especial.
        - En caso normal, la apuesta debe tener mayor cantidad o igual cantidad con pinta superior.

        Args:
            nueva_apuesta (Apuesta): La apuesta que se desea validar.
            apuesta_anterior (Apuesta or None): La apuesta previa en la ronda.
            jugador (Jugador): El jugador que realiza la apuesta.

        Returns:
            bool: True si la apuesta es válida, False si no.
        """
        pinta_actual = nueva_apuesta.pinta
        cantidad_actual = nueva_apuesta.cantidad
        num_dados = jugador.cacho.num_dados

        if apuesta_anterior is None:
            return ValidadorApuesta._validar_apuesta_inicial(pinta_actual, num_dados)

        pinta_anterior = apuesta_anterior.pinta
        cantidad_anterior = apuesta_anterior.cantidad

        # Cambio hacia "As"
        if pinta_actual == "As" and pinta_anterior != "As":
            cantidad_convertida = ValidadorApuesta._convertir_a_ases(cantidad_anterior)
            return cantidad_actual >= cantidad_convertida

        # Cambio desde "As"
        if pinta_anterior == "As" and pinta_actual != "As":
            cantidad_convertida = ValidadorApuesta._convertir_desde_ases(cantidad_anterior)
            return cantidad_actual >= cantidad_convertida

        # Apuesta normal
        return (cantidad_actual > cantidad_anterior) or (
            cantidad_actual == cantidad_anterior and
            ValidadorApuesta._pinta_mayor(pinta_actual, pinta_anterior)
        )

    @staticmethod
    def _validar_apuesta_inicial(pinta, num_dados):
        """
        Valida si una apuesta inicial es legal.

        Regla especial:
        - No se puede iniciar con "As" si el jugador tiene más de 1 dado.

        Args:
            pinta (str): Pinta de la apuesta.
            num_dados (int): Número de dados del jugador.

        Returns:
            bool: True si es válida, False si no.
        """
        if pinta == "As" and num_dados > 1:
            return False
        return True

    @staticmethod
    def _convertir_a_ases(cantidad):
        """
        Convierte una apuesta con pinta normal a su equivalente en "Ases".

        Reglas:
        - Si cantidad es par: cantidad / 2 + 1
        - Si cantidad es impar: redondear hacia arriba

        Args:
            cantidad (int): Cantidad de la apuesta anterior.

        Returns:
            int: Cantidad mínima de "Ases" requerida.
        """
        if cantidad % 2 == 0:
            return cantidad // 2 + 1
        else:
            return math.ceil(cantidad / 2)

    @staticmethod
    def _convertir_desde_ases(cantidad):
        """
        Convierte una apuesta con "Ases" a su equivalente en pintas normales.

        Regla:
        - cantidad * 2 + 1

        Args:
            cantidad (int): Cantidad de "Ases" apostados.

        Returns:
            int: Cantidad mínima de otra pinta requerida.
        """
        return cantidad * 2 + 1

    @staticmethod
    def _pinta_mayor(pinta_nueva, pinta_anterior):
        """
        Determina si la pinta nueva tiene mayor jerarquía que la anterior.

        Jerarquía definida por Dado.PINTA (1 = As, 6 = Sexto).

        Args:
            pinta_nueva (str): Pinta de la nueva apuesta.
            pinta_anterior (str): Pinta de la apuesta anterior.

        Returns:
            bool: True si la nueva pinta es superior, False si no.
        """
        pinta_inversa = {v: k for k, v in Dado.PINTA.items()}
        return pinta_inversa[pinta_nueva] > pinta_inversa[pinta_anterior]
