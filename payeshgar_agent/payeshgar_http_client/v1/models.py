import json
from typing import Union


class DTO:
    fields = ""
    _fields_list = []

    def __init__(self, **kwargs):
        self._fields_list = [f.strip() for f in self.fields.split(",")]
        for field in self._fields_list:
            setattr(self, field, kwargs[field])

    def as_json(self):
        return json.dumps({field: getattr(self, field) for field in self._fields_list})


class AgentDTO(DTO):
    fields = "name, country, groups"
