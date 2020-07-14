import json
from datetime import datetime
from typing import Optional, List

import requests
from payeshgar_http_client.v1 import models


class PayeshgarServerHTTPClient:
    def __init__(self, base_url: str, token: str):
        v1_prefix = "/api/v1/"
        self.base_url = base_url.strip("/") + v1_prefix
        self.token = token
        self.session = requests.session()
        self.session.headers['X-AGENT-TOKEN'] = token
        self.session.headers['content-type'] = "application/json"

    def _make_url(self, path):
        return self.base_url + path

    def introduce_agent(self, agent: models.AgentDTO):
        url = self._make_url("monitoring/agents")
        response = self.session.post(url, data=agent.as_json(), timeout=5)
        if response.status_code == 400:
            raise Exception("SERVER ERROR: {}".format(str(response.json())))
        if response in (200, 201):
            return

    def get_inspections(self, groups: Optional[list] = None, before: Optional[datetime] = None,
                        after: Optional[datetime] = None):
        url = self._make_url("inspecting/inspections")
        query_params = {}
        if groups:
            query_params['groups'] = groups
        if after:
            query_params['after'] = after
        if before:
            query_params['before'] = before
        response = self.session.get(url, data=query_params, timeout=5)
        if response.status_code == 200:
            return response.json()  # <-- FIXME
        raise Exception("SERVER ERROR: {}".format(response.content))

    def submit_results(self, results: List[dict]):
        url = self._make_url("inspecting/inspection-results?validate=1")  # <-- FIXME remove validate later
        response = self.session.post(url, data=json.dumps(results), timeout=5)
        if response.status_code == 200:
            return
        raise Exception("SERVER ERROR: {}".format(response.content))
