from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaRequestProtocol
from sys import argv
from typing import List


class SellerBehavior(FipaRequestProtocol):
    def __init__(self, agent: Agent) -> None:
        super().__init__(agent=agent, message=None, is_initiator=False)
        self.products: str = "TV 55, Laptop, Microwave"

    def handle_request(self, message: ACLMessage) -> None:
        super().handle_request(message)
        display_message(self.agent.aid.localname, "Received request.")

        response: ACLMessage = message.create_reply()
        response.set_performative(ACLMessage.INFORM)
        response.set_content(self.products)
        self.agent.send(response)


class BuyerBehavior(FipaRequestProtocol):
    def __init__(self, agent: Agent, message: ACLMessage) -> None:
        super().__init__(agent=agent, message=message, is_initiator=True)

    def handle_inform(self, message: ACLMessage) -> None:
        display_message(self.agent.aid.localname, message.content)


class TimedBehavior(TimedBehaviour):
    def __init__(self, agent: Agent, interval: float, message: ACLMessage) -> None:
        super().__init__(agent, interval)
        self.message: ACLMessage = message

    def on_time(self) -> None:
        super().on_time()
        self.agent.send(self.message)


class SellerAgent(Agent):
    def __init__(self, aid: AID) -> None:
        super().__init__(aid=aid)
        self.behaviors = SellerBehavior(self)
        self.behaviours.append(self.behaviors)


class BuyerAgent(Agent):
    def __init__(self, aid: AID, receiver: str) -> None:
        super().__init__(aid=aid)

        message: ACLMessage = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name=receiver))
        message.set_content("products")

        self.request_behavior = BuyerBehavior(self, message)
        self.timed_behavior = TimedBehavior(self, 8.0, message)

        self.behaviours.append(self.request_behavior)
        self.behaviours.append(self.timed_behavior)


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python script.py <start_port>")
        exit(1)

    num_agents: int = 1
    port_offset: int = 500
    agents: List[Agent] = []

    for i in range(num_agents):
        port: int = int(argv[1]) + (i * port_offset)

        seller_name: str = f"seller_agent_{port}@localhost:{port}"
        seller_agent = SellerAgent(AID(name=seller_name))
        agents.append(seller_agent)

        buyer_port: int = port - 10000
        buyer_name: str = f"buyer_agent_{buyer_port}@localhost:{buyer_port}"
        buyer_agent = BuyerAgent(AID(name=buyer_name), seller_name)
        agents.append(buyer_agent)

    start_loop(agents)
