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
    def __init__(self, taulell, pes: int, jugador: TipusCasella, pare: None):
        self.__info = taulell
        self.__pes = pes
        self.__pare = pare
        self.__torn = jugador

    def __hash__(self):
        return hash(tuple(self.__info))

    def es_meta(self) -> bool:
        pass


    def genera_fills(self) -> list:
        fills = []

        return fills

    def __str__(self):
        return str(self.__info)

class Agent(joc.Agent):
    def __init__(self, nom):
        super(Agent, self).__init__(nom)

    def pinta(self, display):
        pass

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador

        print(jugador)
        prova = Estat(taulell, 0, jugador, None)
        print(prova)
        return
