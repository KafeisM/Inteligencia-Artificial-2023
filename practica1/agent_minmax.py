from ia_2022 import entorn
from practica1.agent import Estat, Agent
from practica1.entorn import Accio, SENSOR, TipusCasella


class Agent_MinMax(Agent):

    accions = None

    def __init__(self,nom):
        super(Agent_MinMax, self).__init__(nom)
        self.__tancats = set()


    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]
        estat = Estat(taulell, mida[0], jugador, 0, None)

        if self.accions is None:
            estat_aux = self.minmax(estat,3, percepcio)
            while not estat_aux.es_meta():
                estat = Estat(percepcio[SENSOR.TAULELL],mida[0],self.jugador,0,None)
                estat_aux = self.minmax(estat,0,percepcio)
                print(estat_aux)


    def __set_accions(self, estat: Estat):

        accions = list()
        iterador = estat

        while iterador.pare is not None:
            pare, accio = iterador.pare
            accions.insert(0,accio)
            iterador = pare

        if Agent_MinMax.accions is None:
            Agent_MinMax.accions = accions
        else:
            Agent_MinMax.accions += accions

    def minmax(self, estat, profunditat, percepcio) -> Estat:

        es_millor = False

        if estat.es_meta():

            if estat.jugador() == TipusCasella.CREU:
                estat.beta = 1000
            else:
                estat.alpha = -1000
            return estat

        elif profunditat == 3:

            if estat.jugador == TipusCasella.CREU:
                estat.beta = 4 - estat.calc_heuristica() - estat.pes
            else:
                estat.alpha = 4 - estat.calc_heuristica() - estat.pes
            return estat

        fills = estat.genera_fills(percepcio, 2)
        millor_estat = None

        for fill in fills:
            if fill in self.__tancats:
                continue
            fill.alpha = estat.alpha
            fill.beta = estat.beta

            estat_aux = self.minmax(fill, profunditat+1, percepcio)

            if estat_aux is None:
                continue

            es_millor = True

            if estat.jugador == TipusCasella.CARA:
                if estat.alpha < fill.beta and not fill.beta == float('inf'):
                    estat.alpha = fill.beta
                    millor_estat = estat_aux
                if estat.alpha >= estat.beta:
                    millor_estat = None
                    break
            else:
                if estat.beta > fill.alpha and not fill.alpha == float('-inf'):
                    estat.beta = fill.alpha
                    millor_estat = estat_aux
                if estat.alpha >= estat.beta:
                    millor_estat = None
                    break
            self.__tancats.add(fill)

            if es_millor:
                return millor_estat
            else:
                return None

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

