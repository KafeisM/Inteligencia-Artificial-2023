"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import Accio, SENSOR


class Estat:
    def __init__(self, estat: list, pes: int, torn: bool, pare: None):
        self.__info = estat
        self.__pes = pes
        self.__pare = pare
        self.__torn = torn

    def __hash__(self):
        return hash(tuple(self.__info))

    def es_meta(self) -> bool:
        llista = self.__info

        #mirar files
        for fila in llista:
            if '1111' in fila or '2222' in fila:
                return True

        #mirar columnes
        for j in range(len(self.__info[0])):
            columna = ''.join(llista[i][j] for i in range(len(llista)))
            if '1111' in columna or '2222' in columna:
                return True

        #mirar columnes
        for i in range(len(llista) -3):
            for j in range(len(llista[i])-3):
                diagonal1 = ''.join(llista[i+k][j+k] for k in range(4))
                diagonal2 = ''.join(llista[i + k][j+3-k] for k in range(4))
                if '1111' in diagonal1 or '2222' in diagonal1:
                    return True
                if '1111' in diagonal2 or '2222' in diagonal2:
                    return True
        return False


    def genera_fills(self) -> list:
        fills = []
        llista = self.__info
        for fila in llista:
            for valor in fila:
                if valor == '0' and self.__torn:
                    pos = fila.find()

        return fills


    @staticmethod
    def canvia_torn(self):
        self.__torn = not self.__torn

class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def transformar(self, taulell: [[]]) -> list:
        estat = []
        for fila in taulell:
            cadena = [str(numero.value) for numero in fila]
            estat.append("".join(cadena))
        return estat

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]

        prova = Estat(self.transformar(taulell), 0, True, None)
        print(prova.es_meta())
        return
