from agent import Agent
from config import Server, AgentConfig
from exceptions import ValidationError
from repository.repository_factory import RepositoryFactory
from utils import get_key_or_raise


class AgentInitializer:
    """
    AgentInitializer is responsible to create and initialize agent instances
    """

    def __init__(self, configurations: dict):
        self.config = self._create_config_object(configurations)
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
            repository_factory=RepositoryFactory(client),
            groups=server.groups,
        )

    def _create_config_object(self, configurations):
        host_info = get_key_or_raise(
            configurations,
            'host_info',
            ValidationError({'host_info': 'host_info object is required'})
        )
        servers = get_key_or_raise(
            configurations,
            'servers',
            ValidationError({'servers': 'servers list is required'})
        )
        return AgentConfig(host_info=host_info, servers=servers)

    def _get_client(self, server: Server):
        from payeshgar_http_client.v1.client import PayeshgarServerHTTPClient
        return PayeshgarServerHTTPClient(base_url=server.base_url, token=server.token)

    def _introduce_agent(self, client, server):
        from payeshgar_http_client.v1.models import AgentDTO
        dto = AgentDTO(name=self._host_info.name, country=self._host_info.country, groups=server.groups)
        client.introduce_agent(dto)
