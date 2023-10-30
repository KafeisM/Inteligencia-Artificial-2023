from ia_2022 import entorn
from practica1.agent import Estat, Agent
from practica1.entorn import Accio, SENSOR


class Agent_Profunditat(Agent):

    def __init__(self,nom):
        super(Agent_Profunditat,self).__init__(nom)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            self.realitzar_cerca(percepcio)

        if self.__accions is not None:
            for accio in self.__accions:
                _, mov = accio #la accio es una tuple amb Accio a realitzar, (x,y)
                x, y = mov
                self.__accions.remove(accio)
                return Accio.POSAR, (x, y)
        return Accio.ESPERAR

    def realitzar_cerca(self, percepcio):
        self.__accions = []
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]

        estat_inicial = Estat(taulell, mida[0], jugador, None)
        cami, _ = self.cerca_general(estat_inicial,percepcio)  # Realiza la cerca i retorna una array amb els estats

        for meta in cami:
            self.__accions.append(meta.accio()) #guardam les acciones corresponents a cada estat

    def cerca_general(self, estat_inicial,percepcio) -> bool | tuple[entorn.Accio, object]:
        self.__oberts = [(estat_inicial, [])]  # utilitzam una llista i no una coa per la cerca en profunditat
        self.__tancats = set()

        while self.__oberts:
            estat_actual, cami_actual = self.__oberts.pop()

            if estat_actual.es_meta():
                # si l'estat es meta, retornam el cami i que hi ha final
                return cami_actual, True

            succesors = estat_actual.genera_fills(percepcio, 1) #generam fills per nomes 1 jugador
            self.__tancats.add(estat_actual)

            for sucesor in succesors:
                if sucesor not in self.__tancats and sucesor not in (estat for estat, _ in self.__oberts):
                    # Agregamos el sucesor y su camino a la pila
                    nuevo_camino = cami_actual + [sucesor]
                    self.__oberts.append((sucesor, nuevo_camino))

        return [], False  # Si no se troba la meta retorna un cami buid
