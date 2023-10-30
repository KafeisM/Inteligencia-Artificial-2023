from practica1 import agent, joc, aganet_profunditat, agent_a


def main():
    #quatre = joc.Taulell([agent.Agent("Miquel")])
    #quatre = joc.Taulell([aganet_profunditat.Agent_Profunditat("Miquel")])
    quatre = joc.Taulell([agent_a.AgentA("Miquel")])
    quatre.comencar()


if __name__ == "__main__":
    main()
