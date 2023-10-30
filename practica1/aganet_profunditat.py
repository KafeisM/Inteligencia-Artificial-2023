from ia_2022 import entorn
from practica1.agent import Estat, Agent
from practica1.entorn import Accio, SENSOR


class Agent_Profunditat(Agent):

    def __init__(self,nom):
        super(Agent_Profunditat,self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = []

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            self.realitzar_cerca(percepcio)

        if self.__accions is not None:
            for accio in self.__accions:
                _, mov = accio
                x, y = mov  # cada accio es una tupla indicat quants de animals moure
                print(accio)
                self.__accions.remove(accio)
                return Accio.POSAR, (x, y)
        return
    def realitzar_cerca(self, percepcio):
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]

        estat_inicial = Estat(taulell, mida[0], jugador, None)
        cami, _ = self.cerca_general(estat_inicial,percepcio)  # Realiza la búsqueda
        print("pasa")
        for meta in cami:
            print(meta)
            print(meta.accio)
            self.__accions.append(meta.accio())

    def cerca_general(self, estat_inicial,percepcio) -> bool | tuple[entorn.Accio, object]:
        self.__oberts = [(estat_inicial, [])]  # Utilizamos una lista en lugar de una cola para la búsqueda en profundidad
        self.__tancats = set()

        while self.__oberts:
            estat_actual, cami_actual = self.__oberts.pop()  # Utilizamos pop() en lugar de popleft()

            if estat_actual.es_meta():
                # si el estado es meta, retornamos el estado y el camino
                return cami_actual, True

            succesors = estat_actual.genera_fills(percepcio, 1)
            self.__tancats.add(estat_actual)

            for sucesor in succesors:
                if sucesor not in self.__tancats and sucesor not in (estado for estado, _ in self.__oberts):
                    # Agregamos el sucesor y su camino a la pila
                    nuevo_camino = cami_actual + [sucesor]
                    self.__oberts.append((sucesor, nuevo_camino))

        return [], False  # Si no se encuentra la meta, retornamos False
