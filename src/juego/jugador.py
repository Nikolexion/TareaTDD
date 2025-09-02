import random
from src.juego.cacho import Cacho
from abc import ABC, abstractmethod

class Jugador(ABC):
    def __init__(self, nombre):
        self.cacho = Cacho()
        self.nombre = nombre
        self.reglas_especiales = False
    
    @abstractmethod
    def elegir_sentido(self):
        pass
    


class JugadorBot(Jugador):
    def elegir_sentido(self):
        return random.choice(["horario", "antihorario"])
    
    
    
class JugadorHumano(Jugador):
    def elegir_sentido(self):
        while True:
            sentido = input(f"{self.nombre}, Elije el sentido de flujo de juego (horario / antihorario): ").strip().lower()
            if sentido in ["horario", "antihorario"]:
                return sentido
            print("Entrada inválida. Escribe 'horario' o 'antihorario'.")