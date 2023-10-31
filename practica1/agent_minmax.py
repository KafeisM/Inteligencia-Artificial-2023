from ia_2022 import entorn
from practica1.agent import Estat, Agent
from practica1.entorn import Accio, SENSOR, TipusCasella


class Agent_MinMax(Agent):

    def __init__(self,nom):
        super(Agent_MinMax, self).__init__(nom)
        self.__tancats = None


    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]

        estat_inicial = Estat(taulell, mida[0], jugador, 0, None)

        actual, _ = self.minmax(estat_inicial,percepcio)

        mov = actual.pare
        if actual.es_meta() or mov is None:
            return Accio.ESPERAR
        else:
            accio, pos = mov
            return accio, (pos[0], pos[1])

    def minmax(self, estat, percepcio):
        score = self.evaluar(estat)

        if score is not None:
            return estat, score

        puntuacio_fills = [self.minmax(estat_fill,percepcio) for estat_fill in estat.genera_fills(percepcio, 2)]

        if estat.jugador() == TipusCasella.CARA:
            print(puntuacio_fills)
            return max(puntuacio_fills)
        else:
            return min(puntuacio_fills)

    def evaluar(self, estat):
        if estat.es_meta():
            return self.puntuacio(estat)

    def puntuacio(self, estat) -> int:
        matriz = estat.info()
        turno = estat.jugador()
        tamany = estat.tamany()

        for i in range(tamany):
            for j in range(tamany):
                if matriz[i][j] == turno:
                    # Comprueba si hay un Connect 4 en la posición actual
                    if self.hay_connect4(matriz, i, j, turno):
                        return 1  # El jugador actual gana
                    elif matriz[i][j] != TipusCasella.LLIURE:
                        # Comprueba si el oponente tiene un Connect 4 en la posición actual
                        if self.hay_connect4(matriz, i, j, TipusCasella.CARA if turno == TipusCasella.CREU else TipusCasella.CREU):
                            return -1  # El oponente gana

        return 0  # Empate

    def hay_connect4(self, matriz, fila, columna, jugador):
        # Verifica si hay un Connect 4 en la posición actual
        # Comprueba en las 4 direcciones: horizontal, vertical y diagonales
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dr, dc in directions:
            count = 0
            for step in range(-3, 4):
                r, c = fila + dr * step, columna + dc * step
                if 0 <= r < len(matriz) and 0 <= c < len(matriz[0]) and matriz[r][c] == jugador:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

