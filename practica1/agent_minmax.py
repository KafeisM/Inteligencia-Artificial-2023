from ia_2022 import entorn
from practica1.agent import Estat, Agent
from practica1.entorn import Accio, SENSOR, TipusCasella


class Agent_MinMax(Agent):

    accions = None

    def __init__(self,nom):
        super(Agent_MinMax, self).__init__(nom)
        self.__tancats = set()


    def actua(self, percepcio: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        taulell = percepcio[SENSOR.TAULELL]
        jugador = self.jugador
        mida = percepcio[SENSOR.MIDA]
        estat_inicial = Estat(taulell, mida[0], jugador, 0, None)

        millor_mov = self.minmax(estat_inicial,3,percepcio)
        print(millor_mov) #prova

        return Accio.ESPERAR



    def minmax(self, estat, profunditat, percepcio) -> Estat:
        print(estat)
        if estat.es_meta() or profunditat == 0:
            return estat

        if estat.jugador == TipusCasella.CREU:
            millor_valor = float('-inf')
            millor_estat = None
            for fill in estat.genera_fills(percepcio, 2):

                estat_aux = self.minmax(fill, profunditat - 1, percepcio)
                if estat_aux is not None:
                    valor = estat_aux.calc_heuristica() + estat_aux.pes
                    if valor > millor_valor:
                        millor_valor = valor
                        millor_estat = estat_aux
            return millor_estat

        else:  # Jugador CARA

            millor_valor = float('inf')
            millor_estat = None

            for fill in estat.genera_fills(percepcio, 2):
                print(fill)
                estat_aux = self.minmax(fill, profunditat - 1, percepcio)
                print(estat_aux)
                if estat_aux is not None:
                    valor = estat_aux.calc_heuristica() + estat_aux.pes
                    print(valor)
                    if valor < millor_valor:
                        millor_valor = valor
                        millor_valor = estat_aux
            return millor_estat
