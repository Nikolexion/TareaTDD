from src.juego.cacho import Cacho

class Jugador():
    def __init__(self, nombre):
        self.cacho = Cacho()
        self.nombre = nombre
        self.reglas_especiales = False
        
    def elegir_sentido(self):
        return "horario"