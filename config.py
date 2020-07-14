import re
from typing import List
import iso3166
from toml import TomlDecodeError

from utils import validate_url


class ValidationError(ValueError):
    pass


class ConfigFileError(IOError):
    pass


def get_key_or_raise(dictionary: dict, key: str, key_name=None, err_msg=None):
    try:
        return dictionary[key]
    except KeyError:
        key_name = key_name or key
        err_msg = err_msg or "'{}' is required".format(key_name)
        raise ValidationError({key_name: err_msg})


class AgentInfo:
    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country
        self.validate()

    def validate(self):
        name_pattern = '^[a-z0-9-]+$'
        if re.match(name_pattern, self.name) is None:
            raise ValidationError({"agent_info.name": "name should match this pattern '{}'".format(name_pattern)})
        if iso3166.countries_by_alpha3.get(self.country) is None:
            raise ValidationError({"agent_info.country": "country is not a valid iso3166-alpha-3 country code".format(
                name_pattern)})


class Server:
    def __init__(self, base_url: str, token: str, groups: List[str]):
        self.base_url = base_url
        self.token = token
        self.groups = groups
        self.validate()

    def validate(self):
        if validate_url(self.base_url):
            raise ValidationError({"server.base_url": "'{}' is not a valid url".format(self.base_url)})
        if not self.token:
            raise ValidationError({"server.token": "'{}' is not a valid token".format(self.token)})


class AgentConfig:
    def __init__(self, agent_info: dict, servers: List[dict]):
        self.agent_info = AgentInfo(
            name=get_key_or_raise(agent_info, 'name', 'agent_info.name', 'Agent info object must have name'),
            country=get_key_or_raise(agent_info, 'country', 'agent_info.country', 'Agent info object must have country')
        )
        self.servers = []
        for srv in servers:
            self.servers.append(
                Server(
                    base_url=get_key_or_raise(srv, 'base_url', 'servers.base_url', 'All servers must have base_url'),
                    token=get_key_or_raise(srv, 'token', 'servers.token', 'All servers must have token'),
                    groups=get_key_or_raise(srv, 'groups', 'servers.groups', 'All servers must have groups'),
                )
            )

    @staticmethod
    def from_file(file_path):
        import toml
        try:
            configs = toml.load(file_path)
            agent_configuration = AgentConfig(
                agent_info=get_key_or_raise(configs, 'agent_info', 'agent_info', 'agent_info object is required'),
                servers=get_key_or_raise(configs, 'base_url', 'servers.base_url', 'servers list is required'),
            )
            return agent_configuration
        except TomlDecodeError:
            raise ConfigFileError("the configuration file '{}' is not a valid toml file.".format(file_path))
        except Exception:
            raise ConfigFileError("Unable to read the configuration file '{}'".format(file_path))
