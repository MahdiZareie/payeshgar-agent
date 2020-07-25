import json
from datetime import datetime
from typing import Optional, List

import requests
from payeshgar_agent.payeshgar_http_client.v1 import models


class PayeshgarServerHTTPClient:
    def __init__(self, session):
        self.session = session

    def introduce_agent(self, agent: models.AgentDTO):
        url = "monitoring/agents"
        response = self.session.post(url, data=agent.as_json())
        if response.status_code == 400:
            raise Exception("SERVER ERROR: {}".format(str(response.json())))
        if response in (200, 201):
            return

    def _read_paginated_objects(self, relative_url: str, params: dict):
        url = relative_url
        while url is not None:
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                raise Exception("SERVER ERROR: {}".format(response.content))
            data = response.json()
            for item in data['results']:
                yield item
            url = data.get('next')

    def get_inspections(self, groups: Optional[list] = None, before: Optional[datetime] = None,
                        after: Optional[datetime] = None):
        query_params = {}
        if groups:
            query_params['groups'] = groups
        if after:
            query_params['after'] = after
        if before:
            query_params['before'] = before
        return self._read_paginated_objects("inspecting/inspections", query_params)

    def submit_results(self, results: List[dict]):
        url = "inspecting/inspection-results?validate=1"  # <-- FIXME remove validate later
        response = self.session.post(url, data=json.dumps(results), timeout=5)
        if response.status_code == 200:
            return
        raise Exception("SERVER ERROR: {}".format(response.content))

    def get_endpoints(self, groups: Optional[List[str]]):
        query_params = dict(groups=groups) if groups else {}
        return self._read_paginated_objects('monitoring/endpoints', query_params)
