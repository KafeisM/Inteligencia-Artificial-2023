from collections import deque

from ia_2022 import entorn
from practica1 import joc
from practica1.agent import Agent, Estat
from practica1.entorn import Accio, SENSOR, TipusCasella

class AgentAmplada(Agent):

    def __init__(self, nom):
        super(AgentAmplada, self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            self.realitzar_cerca(percepcio)

        if self.__accions is not None:
            for accio in self.__accions:
                x,y = accio #cada accio es una tupla indicat quants de animals moure
                print(accio)
                self.__accions.remove(accio)
                return Accio.POSAR,(x,y)

        return Accio.ESPERAR


    def realitzar_cerca(self, percepcio):
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        estat_inicial = Estat(taulell, 0, jugador, None)

        cami, _ = self.cerca_general(estat_inicial)  # Realiza la búsqueda

        for meta in cami:
            print(meta)

        self.__accions = meta.accions_previes

        print(self.__accions)

    def cerca_general(self,estat_inicial) -> bool | tuple[entorn.Accio,object]:
        self.__oberts = deque([(estat_inicial, [])])  #Utilitzam una tupla per mantenir l'estat i el cami fins ell
        self.__tancats = set()

        while self.__oberts:
            estat_actual, cami_actual = self.__oberts.popleft()

            if estat_actual.es_meta():
                # si l'estat es meta tornam l'estat i el cami
                return cami_actual, True

            succesors = estat_actual.genera_fill()
            self.__tancats.add(estat_actual)

            for sucesor in succesors:
                if sucesor.es_segur():
                    if sucesor not in self.__tancats and sucesor not in (estado for estado, _ in self.__oberts):
                        # Agregam el succesor i el seu cami a la coa
                        nuevo_camino = cami_actual + [sucesor]
                        self.__oberts.append((sucesor, nuevo_camino))

        return [], False  # Si no es troba la meta, tornam false i el cami buit
