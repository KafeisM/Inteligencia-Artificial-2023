from practica1 import agent, joc, agenet_profunditat, agent_a, agent_minmax


def main():
    #quatre = joc.Taulell([agent.Agent("Miquel")])
    #quatre = joc.Taulell([agenet_profunditat.Agent_Profunditat("Miquel")])
    #quatre = joc.Taulell([agent_a.AgentA("Miquel")])
    quatre = joc.Taulell([agent_minmax.Agent_MinMax("Agent1"), agent_minmax.Agent_MinMax("Agent2")])
    quatre.comencar()


if __name__ == "__main__":
    main()
