import requests
from requests import exceptions

from payeshgar_agent.inspectors import BaseInspector


class HTTPInspector(BaseInspector):
    def inspect(self, inspection: dict):
        details = inspection['endpoint']['http_details']
        url = "{protocol}://{hostname}:{port}{path}".format(
            protocol="https" if details['tls'] else 'http',
            hostname=details['hostname'],
            port=details['port'],
            path=details['path']

        )
        return {
            'inspection': inspection['id'],
            **self._send_request(details['method_name'], url, details['maximum_expected_timeout'])
        }

    def _translate_exception(self, exp):
        return {
            exceptions.ConnectTimeout: "TIMEOUT(CONNECT)",
            exceptions.ReadTimeout: "TIMEOUT(READ)",
            exceptions.SSLError: "SLL",
            exceptions.ConnectionError: "CONNECTION",
            exceptions.RetryError: "CONNECTION"
        }.get(type(exp), "UNKNOWN")

    def _get_session(self) -> requests.Session:
        session = requests.session()
        # Customize the session
        return session

    def _send_request(self, method, url, timeout):
        try:
            response = self._get_session().request(method, url, timeout=timeout / 1000)
            return {
                'connection_status': "SUCCEED",
                'status_code': response.status_code,
                'response_time': round(response.elapsed.total_seconds(), 4),
            }
        except Exception as exp:
            return {
                "connection_status": "FAILED",
                "reason": self._translate_exception(exp),
                "note": str(exp)
            }
