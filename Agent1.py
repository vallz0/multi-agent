from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from sys import argv
from typing import List

class TimedBehavior(TimedBehaviour):
    def __init__(self, agent: Agent, interval: float) -> None:
        super().__init__(agent, interval)

    def on_time(self) -> None:
        super().on_time()
        display_message(self.agent.aid.localname, f"Hello from agent {self.agent.aid.localname}")

class CustomAgent(Agent):
    def __init__(self, aid: AID) -> None:
        super().__init__(aid=aid)
        behavior = TimedBehavior(self, 2.0)
        self.behaviours.append(behavior)
        display_message(self.aid.localname, "Hello")

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python script.py <start_port>")
        exit(1)

    num_agents: int = 2
    port_increment: int = 1000
    agents: List[CustomAgent] = []

    for i in range(num_agents):
        port: int = int(argv[1]) + (i * port_increment)
        agent_name: str = f"agent{port}@localhost:{port}"
        agent = CustomAgent(AID(name=agent_name))
        agents.append(agent)

    start_loop(agents)
