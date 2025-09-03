import random
from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import Apuesta
from src.juego.dado import Dado
from src.juego.contador_pintas import Contador_pintas
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.arbitro_ronda import ArbitroRonda
from abc import ABC, abstractmethod

class Jugador(ABC):
    """
    Clase base abstracta para representar un jugador en el juego.

    Atributos:
        nombre (str): Nombre del jugador.
        cacho (Cacho): Contenedor de dados del jugador.
        reglas_especiales (bool): Indica si el jugador está en modo obligado.
        obligado_activado (bool): Flag para saber si ya usó el beneficio de modo obligado.
        modo_obligado (str or None): 'abierto' o 'cerrado' si está obligado, None en caso contrario.

    Métodos abstractos:
        elegir_sentido(): Define el sentido del juego ('horario' o 'antihorario').
        elegir_accion(apuesta_actual): Decide la acción del jugador en su turno.
    """
    def __init__(self, nombre):
        self.cacho = Cacho()
        self.nombre = nombre
        self.reglas_especiales = False
        self.obligado_activado = False
        self.modo_obligado = None  
    
    @abstractmethod
    def elegir_sentido(self):
        """Debe retornar el sentido de juego elegido por el jugador ('horario' o 'antihorario')."""
        pass
    
    @abstractmethod
    def elegir_accion(self, apuesta_actual: Apuesta):
        """Debe retornar un diccionario con la acción elegida: {'tipo': 'apostar'/'dudar'/'calzar', ...}"""
        pass


class JugadorBot(Jugador):
    """
    Representa un jugador automático que toma decisiones basadas en una política greedy.

    Métodos:
        elegir_sentido(): Elige aleatoriamente entre 'horario' y 'antihorario'.
        elegir_accion(apuesta_actual): Decide si apostar, calzar o dudar según su mano y la apuesta actual.
    """
    def elegir_sentido(self):
        return random.choice(["horario", "antihorario"])

    def elegir_accion(self, apuesta_actual: Apuesta):
        """
        Decide la acción del bot en su turno.

        Estrategia:
        - Si no hay apuesta previa, intenta iniciar con la mejor apuesta posible.
        - Si no puede superar la apuesta actual, evalúa si puede calzar.
        - Si no puede calzar, duda.
        - Si tiene opciones válidas, elige la mejor apuesta según cantidad y jerarquía de pinta.

        Returns:
            dict: {'tipo': 'apostar'/'dudar'/'calzar', 'apuesta': Apuesta (si aplica)}
        """
        opciones_validas = []
        ORDEN_PINTAS = [Dado.PINTA[i] for i in sorted(Dado.PINTA.keys())]
        contador = Contador_pintas(self.cacho)

        for pinta in ORDEN_PINTAS:
            cantidad = contador.contar_pintas(pinta, obligar=False)
            if cantidad == 0:
                continue

            nueva_apuesta = Apuesta(cantidad, pinta, self)
            if ValidadorApuesta.es_valida(nueva_apuesta, apuesta_actual, self):
                opciones_validas.append(nueva_apuesta)

        if apuesta_actual is None:
            if opciones_validas:
                mejor_apuesta = max(opciones_validas, key=lambda a: (a.cantidad, ORDEN_PINTAS.index(a.pinta)))
                return {"tipo": "apostar", "apuesta": mejor_apuesta}
            elif self.reglas_especiales:
                raise ValueError(f"{self.nombre} está obligado pero no tiene apuestas válidas")
            else:
                return {"tipo": "dudar"}

        if not opciones_validas:
            arbitro = ArbitroRonda(self, [])  # Solo usamos puede_calzar
            try:
                if arbitro.puede_calzar(apuesta_actual, self):
                    return {"tipo": "calzar"}
            except Exception:
                pass
            return {"tipo": "dudar"}

        mejor_apuesta = max(opciones_validas, key=lambda a: (a.cantidad, ORDEN_PINTAS.index(a.pinta)))
        return {"tipo": "apostar", "apuesta": mejor_apuesta}


class JugadorHumano(Jugador):
    """
    Representa un jugador humano que interactúa por consola.

    Métodos:
        elegir_sentido(): Solicita al usuario que elija el sentido del juego.
        elegir_accion(apuesta_actual): Solicita al usuario que elija una acción y la valida.
    """
    def elegir_sentido(self):
        """
        Solicita al jugador humano que elija el sentido del juego.

        Returns:
            str: 'horario' o 'antihorario'
        """
        while True:
            sentido = input(f"{self.nombre}, Elije el sentido de flujo de juego (horario / antihorario): ").strip().lower()
            if sentido in ["horario", "antihorario"]:
                return sentido
            print("Entrada inválida. Escribe 'horario' o 'antihorario'.")

    def elegir_accion(self, apuesta_actual: Apuesta):
        """
        Solicita al jugador humano que elija una acción en su turno.

        Acciones posibles:
        - 'apostar': el jugador propone una nueva apuesta.
        - 'dudar': el jugador duda de la apuesta actual.
        - 'calzar': el jugador intenta igualar exactamente la apuesta.

        Returns:
            dict: {'tipo': 'apostar'/'dudar'/'calzar', 'apuesta': Apuesta (si aplica)}
        """
        while True:
            accion = input("Elije una jugada a realizar (apostar / dudar / calzar): ").strip().lower()

            if accion == "apostar":
                try:
                    cantidad = int(input("Cantidad: "))
                    pinta = input("Pinta (as, tonto, tren, cuadra, quina, sexto): ").strip().capitalize()
                    nueva_apuesta = Apuesta(cantidad, pinta, self)

                    if ValidadorApuesta.es_valida(nueva_apuesta, apuesta_actual, self):
                        return {"tipo": "apostar", "apuesta": nueva_apuesta}
                    else:
                        print("Apuesta inválida. Debe superar la anterior en cantidad o en pinta.")
                except Exception:
                    print("Entrada inválida. Intenta nuevamente.")

            elif accion == "dudar":
                return {"tipo": "dudar"}

            elif accion == "calzar":
                return {"tipo": "calzar"}

            else:
                print("Jugada inválida. Escribe 'apostar', 'dudar' o 'calzar'.")
