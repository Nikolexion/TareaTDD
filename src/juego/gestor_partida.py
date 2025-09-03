import random

from src.juego.jugador import Jugador, JugadorBot, JugadorHumano
from src.juego.dado import Dado
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.validador_apuesta import ValidadorApuesta

class GestorPartida:
    """
    Clase encargada de coordinar el flujo completo de una partida.

    Administra:
    - Jugadores y turnos
    - Sentido del juego
    - Reglas especiales (modo obligado)
    - Determinación del jugador inicial
    - Visibilidad de dados según tipo de jugador y modo

    Atributos:
        jugadores (list[Jugador]): Lista de jugadores en la partida.
        jugador_inicial (Jugador): Jugador que inicia la ronda actual.
        sentido (str): 'horario' o 'antihorario'.
        turno_index (int): Índice del jugador actual en orden_turnos.
        jugador_afectado (Jugador or None): Jugador que perdió o ganó dado en la ronda anterior.
        orden_turnos (list[Jugador]): Lista ordenada de jugadores activos según sentido.
        ronda_obligada (bool): Indica si el jugador inicial está obligado.
        apuesta_actual (Apuesta or None): Última apuesta realizada en la ronda.
    """

    def __init__(self, jugadores: Jugador):
        self.jugadores = jugadores
        self.jugador_inicial = None
        self.sentido = "horario"
        self.turno_index = 0
        self.jugador_afectado = None
        self.orden_turnos = []
        self.ronda_obligada = False
        self.apuesta_actual = None

    def establecer_jugador_afectado(self, jugador: Jugador):
        """
        Registra el jugador que fue afectado (perdió o ganó dado) en la ronda anterior.
        """
        self.jugador_afectado = jugador

    def definir_sentido(self, sentido: str):
        """
        Establece el sentido de juego.

        Args:
            sentido (str): 'horario' o 'antihorario'.

        Raises:
            ValueError: Si el sentido no es válido.
        """
        if sentido not in ["horario", "antihorario"]:
            raise ValueError("Sentido debe ser 'horario' o 'antihorario'")
        self.sentido = sentido

    def iniciar_ronda(self):
        """
        Inicia una nueva ronda:
        - Agita los dados de todos los jugadores.
        - Verifica si algún jugador entra en modo obligado.
        - Muestra el estado inicial de los dados según visibilidad permitida.
        - Determina si la ronda es obligada.
        - Establece el orden de turnos.
        """
        hay_humano = any(isinstance(j, JugadorHumano) for j in self.jugadores)
        print("\n--- Iniciando nueva ronda ---")
        for jugador in self.jugadores:
            jugador.cacho.agitar()
            self.verificar_reglas_especiales(jugador)

        print("\nEstado inicial de la ronda:")
        humano_obligado = next((j for j in self.jugadores if isinstance(j, JugadorHumano) and j.reglas_especiales), None)

        for jugador in self.jugadores:
            if hay_humano:
                if isinstance(jugador, JugadorHumano):
                    if jugador.reglas_especiales and jugador.modo_obligado == "abierto":
                        print(f"{jugador.nombre} tiene {jugador.cacho.numero_dados()} dados.")
                    else:
                        print(f"{jugador.nombre} tiene {jugador.cacho.numero_dados()} dados: {[d.pinta() for d in jugador.cacho.dados]}")
                else:
                    if humano_obligado and humano_obligado.modo_obligado == "abierto":
                        print(f"{jugador.nombre} tiene {jugador.cacho.numero_dados()} dados: {[d.pinta() for d in jugador.cacho.dados]}")
                    else:
                        print(f"{jugador.nombre} tiene {jugador.cacho.numero_dados()} dados.")
            else:
                print(f"{jugador.nombre} tiene {jugador.cacho.numero_dados()} dados: {[d.pinta() for d in jugador.cacho.dados]}")

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
        """
        Calcula el orden de turnos para la ronda actual según el sentido de juego.

        Returns:
            list[Jugador]: Lista ordenada de jugadores activos.
        """
        activos = [j for j in self.jugadores if j.cacho.numero_dados() > 0]

        if self.jugador_inicial not in activos:
            self.jugador_inicial = activos[0]

        idx = activos.index(self.jugador_inicial)

        if self.sentido == "horario":
            return activos[idx:] + activos[:idx]
        else:
            return list(reversed(activos[:idx+1])) + list(reversed(activos[idx+1:]))

    def obtener_jugador_actual(self):
        """
        Retorna el jugador que tiene el turno actual.

        Returns:
            Jugador: Jugador en turno.
        """
        return self.orden_turnos[self.turno_index]

    def avanzar_turno(self):
        """
        Avanza al siguiente jugador en el orden de turnos.
        """
        self.turno_index = (self.turno_index + 1) % len(self.orden_turnos)

    def verificar_reglas_especiales(self, jugador):
        """
        Verifica si el jugador debe activar el modo obligado.

        Reglas:
        - Se activa si el jugador tiene solo 1 dado y nunca ha usado el beneficio.

        Args:
            jugador (Jugador): Jugador a verificar.
        """
        num_dados = jugador.cacho.num_dados

        if num_dados == 1 and not jugador.obligado_activado:
            jugador.reglas_especiales = True
            jugador.obligado_activado = True
            jugador.modo_obligado = self.pedir_modo_obligado(jugador)
        else:
            jugador.reglas_especiales = False

    def determinar_jugador_inicial(self):
        """
        Determina el jugador que inicia la partida mediante tiradas de dado.

        En caso de empate, se repite la tirada solo entre los empatados.

        También permite al jugador inicial elegir el sentido del juego.
        """
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
        """
        Verifica si la partida ha terminado.

        La partida se considera terminada cuando solo queda un jugador con dados.

        Returns:
            bool: True si hay un único jugador activo, False en caso contrario.
        """
        jugadores_activos = [j for j in self.jugadores if j.cacho.numero_dados() > 0]
        return len(jugadores_activos) == 1


    def pedir_modo_obligado(self, jugador):
        """
        Solicita al jugador que elija el modo de juego cuando está obligado.

        Reglas:
        - Si el jugador es un bot, elige aleatoriamente entre 'abierto' y 'cerrado'.
        - Si el jugador es humano, se le solicita por consola hasta que ingrese una opción válida.

        Args:
            jugador (Jugador): El jugador que debe elegir el modo obligado.

        Returns:
            str: 'abierto' o 'cerrado'
        """
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
        """
        Inicia la partida completa.

        Reglas:
        - Debe haber al menos 2 jugadores.
        - Se determina el jugador inicial mediante tiradas de dado.
        - Se ejecutan rondas hasta que solo quede un jugador con dados.
        - Al final, se anuncia el ganador.

        Raises:
            ValueError: Si hay menos de 2 jugadores.
        """
        if len(self.jugadores) < 2:
            raise ValueError("Se requieren al menos 2 jugadores para iniciar la partida")

        self.determinar_jugador_inicial()

        while not self.partida_terminada():
            self.iniciar_ronda()
            self.jugar_ronda()

        ganador = next(j for j in self.jugadores if j.cacho.numero_dados() > 0)
        print(f"\n{ganador.nombre} ha ganado la partida con {ganador.cacho.numero_dados()} dado(s) restante(s)!")


    def jugar_ronda(self, apuesta_inicial_tests=None):
        """
        Ejecuta una ronda completa de juego.

        Flujo:
        - Se establece la apuesta inicial (si se pasa como parámetro).
        - Se itera por los jugadores activos en orden de turno.
        - Cada jugador elige una acción: apostar, dudar o calzar.
        - Se valida la acción y se actualiza el estado del juego.
        - Si hay duda o calzar, se revelan los dados y se determina el jugador afectado.

        Args:
            apuesta_inicial_tests (Apuesta or None): Apuesta inicial para pruebas o simulaciones.
        """
        self.apuesta_actual = apuesta_inicial_tests
        self.arbitro = ArbitroRonda(self.jugador_inicial, self.jugadores)

        print(f"\n--- Jugando ronda ---")
        while True:
            jugador = self.obtener_jugador_actual()
            if jugador.cacho.numero_dados() == 0:
                print(f"{jugador.nombre} no tiene dados. Se salta su turno.")
                self.avanzar_turno()
                continue
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

            elif tipo == "dudar" and self.apuesta_actual is not None:
                print(f"{jugador.nombre} duda de la apuesta: {self.apuesta_actual.cantidad} {self.apuesta_actual.pinta}")
                resultado = self.arbitro.resolver_duda(
                    apuesta=self.apuesta_actual,
                    cacho=jugador.cacho,
                    jugador_duda=jugador,
                    obligar=self.ronda_obligada
                )
                print("\n--- Dados revelados tras la duda ---")
                for j in self.jugadores:
                    print(f"{j.nombre}: {[d.pinta() for d in j.cacho.dados]}")
                print(f"{resultado.pierde_dado.nombre} pierde un dado por dudar.")
                resultado.pierde_dado.cacho.quitar_dado()
                self.establecer_jugador_afectado(resultado.pierde_dado)
                break

            elif tipo == "calzar" and self.apuesta_actual is not None:
                print(f"{jugador.nombre} intenta calzar la apuesta: {self.apuesta_actual.cantidad} {self.apuesta_actual.pinta}")
                if not self.arbitro.puede_calzar(self.apuesta_actual, jugador):
                    print(f"\n{jugador.nombre} no puede calzar esta apuesta. Debe tener solo 1 dado o que la apuesta sea al menos la mitad de los dados en juego.")
                    continue
                resultado = self.arbitro.resolver_calzar(
                    apuesta=self.apuesta_actual,
                    cacho=jugador.cacho,
                    jugador_calza=jugador,
                    obligar=self.ronda_obligada
                )

                print("\n--- Dados revelados tras intentar calzar ---")
                for j in self.jugadores:
                    print(f"{j.nombre}: {[d.pinta() for d in j.cacho.dados]}")

                if resultado.acierta:
                    print(f"{jugador.nombre} calzó justo. Recupera un dado.")
                    resultado.recupera_jugador.cacho.sumar_dado()
                else:
                    print(f"{jugador.nombre} falló al calzar. Pierde un dado.")
                    resultado.pierden_dado[0].cacho.quitar_dado()

                self.establecer_jugador_afectado(jugador)
                break

            else:
                print("Acción inválida. Intente nuevamente")
