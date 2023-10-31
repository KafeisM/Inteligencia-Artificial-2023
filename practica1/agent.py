"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR, TipusCasella


class Estat:
    def __init__(self, taulell, tamany, jugador: TipusCasella, pes: int, pare: None):
        self.__info = taulell
        self.__pare = pare
        self.__torn = jugador
        self.__pes = pes
        self.__n = tamany

    def __str__(self):
        matriu_str = '\n'.join([' '.join([str(TipusCasella(value).name) for value in row]) for row in self.__info])
        return f"{matriu_str} \nTorn del jugador: {self.__torn}"

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.__info == other.__info

    def __lt__(self, other):
        """Overrides the less than comparison for A*"""
        return self.__pes < other.__pes

    def __hash__(self):
        return hash(tuple(map(tuple, self.__info)))

    def accio(self):
        return self.__pare

    def jugador(self):
        return self.__torn

    def info(self):
        return self.__info

    def tamany(self):
        return self.__n

    def es_meta(self) -> bool:
        #veificar fies
        for fila in self.__info:
            if self._verificar_fila(fila):
                return True

        #verificar columnes
        for col in range(self.__n):
            columna = [fila[col] for fila in self.__info]
            if self._verificar_fila(columna):
                return True

        #verificar diagonals
        for i in range(self.__n -3):
            for j in range(self.__n):
                diagonal = [self.__info[i+k][i+k] for k in range(4)]
                if self._verificar_fila(diagonal):
                    return True

                diagonal = [self.__info[i+k][j-k] for k in range(4) if j-k >=0]
                if self._verificar_fila(diagonal):
                    return True
        return False

    def _verificar_fila(self, linea):
        for i in range(len(linea) -3):
            if all(casella == self.__torn for casella in linea[i:i +4]):
                return True
        return False

    def genera_fills(self, percepcio:entorn.Percepcio, numJugs: int) -> list:
        fills = []
        matriu = self.__info
        files,columnes = percepcio[SENSOR.MIDA]

        for i in range(files):
            for j in range(columnes):
                if matriu[i][j] is TipusCasella.LLIURE and numJugs == 1:
                    matriz_auxiliar = [fila[:] for fila in matriu]
                    matriz_auxiliar[i][j] = TipusCasella.CARA
                    fills.append(Estat(matriz_auxiliar,files,TipusCasella.CARA,self.__pes+1 ,(Accio.POSAR,(j,i))))

                elif matriu[i][j] is TipusCasella.LLIURE and numJugs == 2:
                    matriz_auxiliar = [fila[:] for fila in matriu]
                    if self.__torn == TipusCasella.CARA:
                        matriz_auxiliar[i][j] = TipusCasella.CARA
                        seguent = TipusCasella.CREU
                    else:
                        matriz_auxiliar[i][j] = TipusCasella.CREU
                        seguent = TipusCasella.CARA

                    fills.append(Estat(matriz_auxiliar,files,seguent,self.__pes+1 ,(Accio.POSAR, (j, i))))
        return fills

    def calc_heuristica(self, percepcio: entorn.Percepcio) -> int:
        n,m = percepcio[SENSOR.MIDA]

        def contar_seguits(linea):
            maxim = 0
            cont = 0

            for valor in linea:
                if valor == self.__torn.value:
                    cont += 1
                    maxim = max(maxim, cont)
                else:
                    cont = 0
            return maxim

        files_rest = [4 - contar_seguits(self.__info[i]) for i in range(n)]
        columnes_rest = [4 - contar_seguits([self.__info[i][j] for i in range(n)]) for j in range(m)]
        diagonal_rest = []

        for i in range(self.__n -3):
            for j in range(self.__n):
                diagonal = [self.__info[i+k][i+k] for k in range(4)]
                diagonal_rest.append(4 - contar_seguits(diagonal))
                diagonal = [self.__info[i+k][j-k] for k in range(4) if j-k >=0]
                diagonal_rest.append(4 - contar_seguits(diagonal))
        return (min(min(files_rest), min(columnes_rest), min(diagonal_rest))) + self.__pes

class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]

        prova = Estat(taulell, mida[0], jugador,None)
        print(prova.es_meta())

        return
