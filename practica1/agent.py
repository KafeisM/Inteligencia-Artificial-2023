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
    def __init__(self, taulell, tamany, jugador: TipusCasella, pes: int, pare=None):
        self.__info = taulell
        self.__pare = pare
        self.__torn = jugador
        self.__pes = pes
        self.__n = tamany
        self.__alpha = float('-inf')
        self.__beta = float('inf')
        self.__utilitat = 0

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

    @property
    def pare(self):
        return self.__pare

    @property
    def alpha(self):
        return self.__alpha

    @property
    def beta(self):
        return self.__beta

    @property
    def utilitat(self):
        return self.__utilitat

    @property
    def pes(self):
        return self.__pes

    @alpha.setter
    def alpha(self, alpha):
        self.__alpha = alpha

    @beta.setter
    def beta(self, beta):
        self.__beta = beta

    @utilitat.setter
    def utilitat(self, utilitat):
        self.__utilitat = utilitat

    @property
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
                    fills.append(Estat(matriz_auxiliar,files,TipusCasella.CARA,self.__pes+1 ,(self,(Accio.POSAR,(j,i)))))

                elif matriu[i][j] is TipusCasella.LLIURE and numJugs == 2:
                    matriz_auxiliar = [fila[:] for fila in matriu]
                    if self.__torn == TipusCasella.CARA:
                        matriz_auxiliar[i][j] = TipusCasella.CARA
                        seguent = TipusCasella.CREU
                    else:
                        matriz_auxiliar[i][j] = TipusCasella.CREU
                        seguent = TipusCasella.CARA

                    fills.append(Estat(matriz_auxiliar,files,seguent,self.__pes+1 ,(self,(Accio.POSAR, (j, i)))))
        return fills

    def __contar_seguits_recte(self, pos_1, pos_2, reverse=False) -> int:
        continu = False
        count = 0
        best_lineal = 0
        for x in range(max(pos_1 - 4, 0), min(pos_1 + 4, self.__n), 1):
            if reverse:
                tipus = self.__info[pos_2][x]
            else:
                tipus = self.__info[x][pos_2]

            if tipus is self.__torn:
                if not continu:
                    continu = True
                count += 1
            else:
                continu = False
                if count > best_lineal:
                    best_lineal = count
                count = 0

        if count > best_lineal:
            best_lineal = count

        return best_lineal

    def __contar_seguits_diag(self, pos_1, pos_2, desp: tuple) -> int:
        continu = False
        count = 0
        best_lineal = 0

        for i, j in zip(
                range(pos_1 - (4 * desp[0]), pos_1 + (4 * desp[0]), desp[0]),
                range(pos_2 - (4 * desp[1]), pos_2 + (4 * desp[1]), desp[1])
        ):
            if not (0 <= i < len(self.__info) and 0 <= j < len(self.__info[0])):
                continue

            if self.__info[i][j] is self.__torn:
                if not continu:
                    continu = True
                count += 1
            else:
                continu = False
                if count > best_lineal:
                    best_lineal = count
                count = 0
        if count > best_lineal:
            best_lineal = count

        return best_lineal

    def calc_heuristica(self) -> int:

        res = 0
        maxim = 0
        self.__utilitat = 0
        if self.__pare is not None:
            for i in range(self.__n):
                for j in range(self.__n):
                    horizontal = self.__contar_seguits_recte(i,j,True)
                    vertical = self.__contar_seguits_recte(i,j,False)
                    diag1 = self.__contar_seguits_diag(i,j,(1,1))
                    diag2 = self.__contar_seguits_diag(i,j,(1,-1))
                    maxim = max(horizontal, vertical, diag1, diag2)
                    if maxim > res:
                        res = maxim
        return 4 - res + self.__pes



class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass
