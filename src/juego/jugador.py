import random
from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import Apuesta
from src.juego.dado import Dado
from src.juego.contador_pintas import Contador_pintas
from src.juego.validador_apuesta import ValidadorApuesta
from src.juego.arbitro_ronda import ArbitroRonda
from abc import ABC, abstractmethod


class Jugador(ABC):
    def __init__(self, nombre):
        self.cacho = Cacho()
        self.nombre = nombre
        self.reglas_especiales = False
        self.obligado_activado = False  # flag para saber si ya usó el beneficio por una vez
        self.modo_obligado = None  
    
    @abstractmethod
    def elegir_sentido(self):
        pass
    
    @abstractmethod
    def elegir_accion(self, apuesta_actual: Apuesta):
        pass
    


##Jugador que juega por sí solo
class JugadorBot(Jugador):
    def elegir_sentido(self):
        return random.choice(["horario", "antihorario"])

    
    ##metodo que sigue una política greedy
    def elegir_accion(self, apuesta_actual: Apuesta):
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
            arbitro = ArbitroRonda(self, [])  # jugadores vacíos porque solo usamos puede_calzar
            try:
                if arbitro.puede_calzar(apuesta_actual, self):
                    return {"tipo": "calzar"}
            except Exception:
                pass
            return {"tipo": "dudar"}

        # Tiene opciones válidas para apostar
        mejor_apuesta = max(opciones_validas, key=lambda a: (a.cantidad, ORDEN_PINTAS.index(a.pinta)))
        return {"tipo": "apostar", "apuesta": mejor_apuesta}



##Jugador que puede tomar acciones interactuando por consola
class JugadorHumano(Jugador):
    def elegir_sentido(self):
        while True:
            sentido = input(f"{self.nombre}, Elije el sentido de flujo de juego (horario / antihorario): ").strip().lower()
            if sentido in ["horario", "antihorario"]:
                return sentido
            print("Entrada inválida. Escribe 'horario' o 'antihorario'.")
            
    def elegir_accion(self, apuesta_actual: Apuesta):
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
