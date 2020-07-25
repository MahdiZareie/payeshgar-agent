from payeshgar_agent.agent import Agent
from payeshgar_agent.config import Server, AgentConfig

from payeshgar_agent.payeshgar_http_client.v1.client import PayeshgarServerHTTPClient


class AgentInitializer:
    """
    AgentInitializer is responsible to create and initialize agent instances
    """

    def __init__(self, configurations: dict):
        self.config = AgentConfig(configurations)
        self._host_info = self.config.host_info
        self._servers = self.config.servers

    def initialize(self) -> list:
        agents = []
        for server in self._servers:
            agents.append(self._initialize_server(server))
        return agents

    def _initialize_server(self, server: Server):
        client = self._get_client(server)
        self._introduce_agent(client, server)
        return Agent(
            client=client,
            groups=server.groups,
        )

    def _get_client(self, server: Server) -> PayeshgarServerHTTPClient:
        return PayeshgarServerHTTPClient(base_url=server.base_url, credentials=server.credentials)

    def _introduce_agent(self, client, server):
        from payeshgar_agent.payeshgar_http_client.v1.models import AgentDTO
        dto = AgentDTO(name=self._host_info.name, country=self._host_info.country, groups=server.groups)
        client.introduce_agent(dto)
