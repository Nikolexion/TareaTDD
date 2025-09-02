import random
from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import Apuesta
from abc import ABC, abstractmethod

class Jugador(ABC):
    def __init__(self, nombre):
        self.cacho = Cacho()
        self.nombre = nombre
        self.reglas_especiales = False
    
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
    
    def elegir_accion(self, apuesta_actual: Apuesta):
        #como la apuesta inicial
        pinta = self.cacho.dados[0].pinta()
        cantidad = 1
        apuesta = Apuesta(cantidad=cantidad, pinta=pinta, jugador_que_aposto=self)
        return {"tipo": "apostar", "apuesta": apuesta}
    
    

##Jugador que puede tomar acciones interactuando por consola
class JugadorHumano(Jugador):
    def elegir_sentido(self):
        while True:
            sentido = input(f"{self.nombre}, Elije el sentido de flujo de juego (horario / antihorario): ").strip().lower()
            if sentido in ["horario", "antihorario"]:
                return sentido
            print("Entrada inválida. Escribe 'horario' o 'antihorario'.")
            
    def elegir_accion(self, apuesta_actual: Apuesta):
        accion = input("Elije una jugada a realizar (apostar / dudar / calzar): ").strip().lower()

        if accion == "apostar":
            cantidad = int(input("Cantidad: "))
            pinta = input("Pinta (As, Tonto, Tren, Cuadra, Quina, Sexto): ").strip().capitalize()
            apuesta = Apuesta(cantidad=cantidad, pinta=pinta, jugador_que_aposto=self)
            return {"tipo": "apostar", "apuesta": apuesta}

        elif accion == "dudar":
            return {"tipo": "dudar"}

        elif accion == "calzar":
            return {"tipo": "calzar"}

        else:
            raise ValueError("Jugada inválida. Las jugadas son 'apostar', 'dudar' y 'calzar'")

