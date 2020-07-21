"""
This module contains the classes which describe the structure of configurations.
These classes designed to validate input config values

"""
import re
from typing import List
import iso3166

from exceptions import ValidationError
from utils import validate_url, get_key_or_raise


class HostInfo:
    """
    This class represents Host information in the configuration
    """
    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country
        self.validate()

    def validate(self):
        name_pattern = '^[a-z0-9-]+$'
        if re.match(name_pattern, self.name) is None:
            raise ValidationError({"host_info.name": "name should match this pattern '{}'".format(name_pattern)})
        if iso3166.countries_by_alpha3.get(self.country) is None:
            raise ValidationError({"host_info.country": "country is not a valid iso3166-alpha-3 country code".format(
                name_pattern)})


class Server:
    """
    This class represents a server object in the configurations
    """
    def __init__(self, base_url: str, credentials: dict, groups: List[str]):
        self.base_url = base_url
        self.credentials = credentials
        self.groups = groups
        self.validate()

    def validate(self):
        if not validate_url(self.base_url):
            raise ValidationError({"server.base_url": "'{}' is not a valid url".format(self.base_url)})
        if not self.credentials:
            raise ValidationError({"server.credentials": "credentials is required"})


class AgentConfig:
    """
    This class represents complete configurations of the agent
    """
    def __init__(self, host_info: dict, servers: List[dict]):
        host_name = get_key_or_raise(
            host_info,
            'name',
            ValidationError({'host_info.name': 'Host info object must have name'})
        )
        host_country = get_key_or_raise(
            host_info,
            'country',
            ValidationError({'host_info.country': 'Host info object must have country'})
        )

        self.host_info = HostInfo(
            name=host_name,
            country=host_country
        )
        self.servers = []
        for srv in servers:
            base_url = get_key_or_raise(
                srv,
                'base_url',
                ValidationError({'servers.base_url': 'All servers must have base_url'})
            )
            credentials = get_key_or_raise(
                srv,
                'credentials',
                ValidationError({'servers.credentials': 'All servers must have credentials'})
            )
            groups = get_key_or_raise(
                srv,
                'groups',
                ValidationError({'servers.groups': 'All servers must have groups'})
            )

            self.servers.append(
                Server(
                    base_url=base_url,
                    credentials=credentials,
                    groups=groups,
                )
            )
