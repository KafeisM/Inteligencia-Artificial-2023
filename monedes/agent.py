""" Mòdul que conté l'agent per jugar al joc de les monedes.

Percepcions:
    ClauPercepcio.MONEDES
Solució:
    " XXXC"
"""
from queue import PriorityQueue

from ia_2022 import agent, entorn
from monedes.entorn import AccionsMoneda, SENSOR

SOLUCIO = " XXXC"

class Estat:

    def __init__(self, estat: str, pes: int, pare=None):
        self.__info = estat
        self.__pes = pes
        self.__pare = pare

    def __hash__(self):
        return hash(tuple(self.__info))

    def __eq__(self, other):
        """Overrides the default implementation"""
        return self.__info == other.info

    #GETERS
    @property
    def info(self):
        return self.__info

    @property
    def pare(self):
        return self.__pare

    #SETERS
    @pare.setter
    def pare(self, value):
        self.__pare = value

    @staticmethod
    def gira(moneda):
        if moneda == "C":
            return "X"
        elif moneda == "X":
            return "C"
        else:
            return " "

    def es_meta(self) -> bool:
        return self.__info == SOLUCIO

    def calc_heuristica(self) -> int:
        pos = self.__info.find(" ")
        heuristica = 0

        for lletra_es, lletra_sol in zip(self.__info, SOLUCIO):
            if lletra_sol != " ":
                heuristica += int(lletra_es != lletra_sol)

        heuristica += pos

        return heuristica + self.__pes #realment retorna el f(n)

    def genera_fills(self):
        fills = []

        buit = self.__info.find(" ")

        despls = [buit - 1, buit + 1]
        for desp in despls:
            if -1 < desp < len(self.__info):
                info_aux = list(self.__info)
                info_aux[buit] = self.__info[desp]
                info_aux[desp] = " "

                fills.append(
                    Estat(
                        "".join(info_aux),
                        self.__pes + 1,
                        (self, (AccionsMoneda.DESPLACAR, desp)),
                        )
                )

        for i in range(len(self.__info)):
            info_aux = list(self.__info)
            info_aux[i] = self.gira(info_aux[i])
            fills.append(
                Estat(
                    "".join(info_aux), self.__pes + 2, (self, (AccionsMoneda.GIRAR, i))
                )
            )

        despls = [buit - 2, buit + 2]
        for desp in despls:
            if -1 < desp < len(self.__info):
                info_aux = list(self.__info)
                info_aux[buit] = self.gira(self.__info[desp])
                info_aux[desp] = " "

                fills.append(
                    Estat(
                        "".join(info_aux),
                        self.__pes + 2,
                        (self, (AccionsMoneda.BOTAR, desp)),
                        )
                )

        return fills

    def __lt__(self, other):
        return False

    def __str__(self):
        return str(self.__info)


class AgentMoneda(agent.Agent):
    def __init__(self):
        super().__init__(long_memoria=0)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)

    def cerca(self, estat_inicial):
        self.__oberts = PriorityQueue() #coa amb prioritat (sempre visible el proxim per agafar es a dir f(n) menor)
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(), estat_inicial)) #tupla amb la heuristica i l'estat

        actual = None
        while not self.__oberts.empty():
            _, actual = self.__oberts.get()
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            fills = actual.genera_fills()

            for fill in fills:
                self.__oberts.put((fill.calc_heuristica(), fill))

            self.__tancats.add(actual)

        if actual.es_meta():
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        inicial = Estat(percepcio[SENSOR.MONEDES], 0, pare=None)

        if self.__accions is None:
            self.cerca(inicial)

        if self.__accions:
            accio = self.__accions.pop()
            return accio[0], accio[1]
        else:
            return AccionsMoneda.RES

