import random

from src.juego.jugador import Jugador, JugadorBot, JugadorHumano
from src.juego.dado import Dado
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.validador_apuesta import ValidadorApuesta

class GestorPartida:
    def __init__(self, jugadores: Jugador):
        self.jugadores = jugadores
        self.jugador_inicial = None
        self.sentido = "horario" #sentido de juego
        self.turno_index = 0
        self.jugador_afectado = None #referencia a jugador que pierde o gana un dado
        self.orden_turnos = []
        self.ronda_obligada = False
        self.apuesta_actual = None

    def establecer_jugador_afectado(self, jugador: Jugador):
        self.jugador_afectado = jugador

    def definir_sentido(self, sentido: str):
        if sentido not in ["horario", "antihorario"]:
            raise ValueError("Sentido debe ser 'horario' o 'antihorario'")
        self.sentido = sentido

    def iniciar_ronda(self):
        #si hay jugador afectado, se define como el que inicia la ronda
        if self.jugador_afectado:
            self.jugador_inicial = self.jugador_afectado
        elif self.jugador_inicial is None:
            raise ValueError("Debe determinarse el jugador inicial antes de iniciar la partida")

        self.orden_turnos = self.obtener_orden_turnos()
        self.turno_index = 0
        self.jugador_afectado = None

    def iniciar_ronda(self):
        print(f"\n--- Iniciando nueva ronda ---")
        for jugador in self.jugadores:
            jugador.cacho.agitar()
            print(f"{jugador.nombre} tiene {jugador.cacho.numero_dados()} dados: {[d.pinta() for d in jugador.cacho.dados]}")
            self.verificar_reglas_especiales(jugador)

        if self.jugador_afectado:
            self.jugador_inicial = self.jugador_afectado
        elif self.jugador_inicial is None:
            raise ValueError("Debe determinarse el jugador inicial antes de iniciar la partida")

        self.ronda_obligada = getattr(self.jugador_inicial, "reglas_especiales", False)
        if self.ronda_obligada:
            print(f"{self.jugador_inicial.nombre} está obligado. Modo: {self.jugador_inicial.modo_obligado}")

        self.orden_turnos = self.obtener_orden_turnos()
        self.turno_index = 0
        self.jugador_afectado = None
        self.apuesta_actual = None



    def obtener_orden_turnos(self):
        idx = self.jugadores.index(self.jugador_inicial)
        if self.sentido == "horario":
            return self.jugadores[idx:] + self.jugadores[:idx]
        else:
            return list(reversed(self.jugadores[:idx+1])) + list(reversed(self.jugadores[idx+1:]))

    def obtener_jugador_actual(self):
        return self.orden_turnos[self.turno_index]

    def avanzar_turno(self):
        self.turno_index = (self.turno_index + 1) % len(self.orden_turnos)

    def verificar_reglas_especiales(self, jugador):
        num_dados = jugador.cacho.num_dados

        # solo activar si tiene 1 dado y nunca ha usado el beneficio
        if num_dados == 1 and not jugador.obligado_activado:
            jugador.reglas_especiales = True
            jugador.obligado_activado = True
            jugador.modo_obligado = self.pedir_modo_obligado(jugador)
        else:
            jugador.reglas_especiales = False

    #para determinar el jugador que empieza la partida y el sentido de juego
    def determinar_jugador_inicial(self):
        tiradas = {}
        ronda = 1
        while True:
            print(f"\n--- Determinando jugador inicial (ronda {ronda}) ---")
            tiradas.clear()
            max_valor = -1
            for jugador in self.jugadores:
                valor = Dado().lanzar()
                print(f"{jugador.nombre} lanza y obtiene: {valor}")
                tiradas.setdefault(valor, []).append(jugador)
                max_valor = max(max_valor, valor)

            if len(tiradas[max_valor]) == 1:
                self.jugador_inicial = tiradas[max_valor][0]
                print(f"{self.jugador_inicial.nombre} será el jugador inicial.")
                sentido = self.jugador_inicial.elegir_sentido()
                print(f"{self.jugador_inicial.nombre} elige el sentido: {sentido}")
                self.definir_sentido(sentido)
                break
            else:
                empatados = [j.nombre for j in tiradas[max_valor]]
                print(f"Empate entre: {empatados}. Se repite la tirada.")
                self.jugadores = tiradas[max_valor]
                ronda += 1


    def partida_terminada(self):
        jugadores_activos = [j for j in self.jugadores if j.cacho.numero_dados() > 0]
        return len(jugadores_activos) == 1
    
    def pedir_modo_obligado(self, jugador):
        print(f"{jugador.nombre} debe elegir modo obligado.")
        if isinstance(jugador, JugadorBot):
            modo = random.choice(["abierto", "cerrado"])
            print(f"{jugador.nombre} (bot) elige modo: {modo}")
            return modo
        elif isinstance(jugador, JugadorHumano):
            while True:
                modo = input(f"{jugador.nombre}, estás obligado. Elije entre modo (abierto/cerrado): ").strip().lower()
                if modo in ["abierto", "cerrado"]:
                    return modo
                print("Entrada inválida. Escribe 'abierto' o 'cerrado'.")

        
        
    def iniciar_partida(self):
        if len(self.jugadores) < 2:
            raise ValueError("Se requieren al menos 2 jugadores para iniciar la partida")

        self.determinar_jugador_inicial()

        while not self.partida_terminada():
            self.iniciar_ronda()
            self.jugar_ronda()    
        
    def jugar_ronda(self, apuesta_inicial_tests=None):
        self.apuesta_actual = apuesta_inicial_tests
        self.arbitro = ArbitroRonda(self.jugador_inicial, self.jugadores)

        print(f"\n--- Jugando ronda ---")
        while True:
            jugador = self.obtener_jugador_actual()
            print(f"\nTurno de {jugador.nombre} ({jugador.cacho.numero_dados()} dados)")

            accion = jugador.elegir_accion(self.apuesta_actual)
            tipo = accion.get("tipo")

            if tipo == "apostar":
                nueva_apuesta = accion["apuesta"]
                print(f"{jugador.nombre} apuesta {nueva_apuesta.cantidad} {nueva_apuesta.pinta}")

                if not ValidadorApuesta.es_valida(nueva_apuesta, self.apuesta_actual, nueva_apuesta.jugador_que_aposto):
                    raise ValueError(f"Apuesta inválida: {nueva_apuesta.cantidad} {nueva_apuesta.pinta}")

                self.apuesta_actual = nueva_apuesta
                self.avanzar_turno()

            elif tipo == "dudar":
                print(f"{jugador.nombre} duda de la apuesta: {self.apuesta_actual.cantidad} {self.apuesta_actual.pinta}")
                resultado = self.arbitro.resolver_duda(
                    apuesta=self.apuesta_actual,
                    cacho=jugador.cacho,
                    jugador_duda=jugador,
                    obligar=self.ronda_obligada
                )
                print(f"{resultado.pierde_dado.nombre} pierde un dado por dudar.")
                resultado.pierde_dado.cacho.quitar_dado()
                self.establecer_jugador_afectado(resultado.pierde_dado)
                break

            elif tipo == "calzar":
                print(f"{jugador.nombre} intenta calzar la apuesta: {self.apuesta_actual.cantidad} {self.apuesta_actual.pinta}")
                resultado = self.arbitro.resolver_calzar(
                    apuesta=self.apuesta_actual,
                    cacho=jugador.cacho,
                    jugador_calza=jugador,
                    obligar=self.ronda_obligada
                )

                if resultado.acierta:
                    print(f"{jugador.nombre} calzó justo. Recupera un dado.")
                    resultado.recupera_jugador.cacho.sumar_dado()
                else:
                    print(f"{jugador.nombre} falló al calzar. Pierde un dado.")
                    resultado.pierden_dado[0].cacho.quitar_dado()

                self.establecer_jugador_afectado(jugador)
                break

            else:
                raise ValueError(f"Jugada desconocida: {tipo}")
