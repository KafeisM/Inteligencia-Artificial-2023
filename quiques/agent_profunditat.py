""" Fitxer que conté l'agent barca en profunditat.

S'ha d'implementar el mètode:
    actua()
"""
from ia_2022 import entorn
from quiques.agent import Barca, Estat
from quiques.entorn import AccionsBarca, SENSOR


class BarcaProfunditat(Barca):
    def __init__(self):
        super(BarcaProfunditat, self).__init__()
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        if self.__accions is None:
            self.realitzar_cerca(percepcio)

        if self.__accions is not None:
            for accio in self.__accions:
                quiques, llops = accio  # cada accio es una tupla indicat quants de animals moure
                print(accio)
                self.__accions.remove(accio)
                return AccionsBarca.MOURE, (quiques, llops)

        return AccionsBarca.ATURAR

    def realitzar_cerca(self, percepcio):
        estat_inicial = Estat(percepcio[SENSOR.LLOC], percepcio[SENSOR.LLOP_ESQ], percepcio[SENSOR.QUICA_ESQ])
        cami, _ = self.cerca_general(estat_inicial)  # Realiza la búsqueda

        for meta in cami:
            print(meta)

        self.__accions = meta.accions_previes

        print(self.__accions)

    def cerca_general(self, estat_inicial) -> bool | tuple[entorn.Accio, object]:
        self.__oberts = [(estat_inicial, [])]  # Utilizamos una lista en lugar de una cola para la búsqueda en profundidad
        self.__tancats = set()

        while self.__oberts:
            estat_actual, cami_actual = self.__oberts.pop()  # Utilizamos pop() en lugar de popleft()

            if estat_actual.es_meta():
                # si el estado es meta, retornamos el estado y el camino
                return cami_actual, True

            succesors = estat_actual.genera_fill()
            self.__tancats.add(estat_actual)

            for sucesor in succesors:
                if sucesor.es_segur():
                    if sucesor not in self.__tancats and sucesor not in (estado for estado, _ in self.__oberts):
                        # Agregamos el sucesor y su camino a la pila
                        nuevo_camino = cami_actual + [sucesor]
                        self.__oberts.append((sucesor, nuevo_camino))

        return [], False  # Si no se encuentra la meta, retornamos False 
