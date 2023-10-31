from queue import PriorityQueue

from ia_2022 import entorn
from practica1.agent import Estat, Agent
from practica1.entorn import Accio, SENSOR

class AgentA(Agent):
    def __init__(self,nom):
        super(AgentA, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        print(self._posicio_pintar)


    def cerca(self, estat_inicial,percepcio):
        self.__oberts = PriorityQueue() #coa amb prioritat (sempre visible el proxim per agafar es a dir f(n) menor)
        self.__tancats = set()

        self.__oberts.put((estat_inicial.calc_heuristica(percepcio), estat_inicial)) #tupla amb la heuristica i l'estat

        actual = None
        while not self.__oberts.empty():
            estimacio, actual = self.__oberts.get()
            print(actual)
            print(estimacio)
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            fills = actual.genera_fills(percepcio, 1)

            for fill in fills:
                self.__oberts.put((fill.calc_heuristica(percepcio), fill))

            self.__tancats.add(actual)

        if actual.es_meta():
            print("hi ha meta")
            accions = []
            iterador = actual

            while iterador.pare is not None:
                pare, accio = iterador.pare

                accions.append(accio)
                iterador = pare
            self.__accions = accions

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]

        estat_inicial = Estat(taulell, mida[0], jugador, 0 ,None)

        if self.__accions is None:
            print("entra")
            self.cerca(estat_inicial,percepcio)
            print("surt")

        if self.__accions:
            accio = self.__accions.pop()
            _, mov = accio  # la accio es una tuple amb Accio a realitzar, (x,y)
            x, y = mov
            return Accio.POSAR, (x,y)
        else:
            return Accio.ESPERAR