import retrying

from payeshgar_agent.payeshgar_http_client.v1.exceptions import InvalidCredentialsException


class JWTAuthentication:
    def __init__(self, credentials, retry_on_failure=3):
        self.username = credentials['username']
        self.password = credentials['password']
        self.auth_header_prefix = 'Bearer'
        self.retryer = retrying.Retrying(
            stop_max_attempt_number=retry_on_failure,
            retry_on_exception=lambda e: not isinstance(e, InvalidCredentialsException)
        )

    def authenticate(self, session):
        session.headers['AUTHORIZATION'] = "{} {}".format(
            self.auth_header_prefix,
            self.retryer.call(self._get_token, session)
        )

    def _get_token(self, session):
        response = session.post(
            url='security/tokens',
            json=dict(username=self.username, password=self.password)
        )
        data = response.json()
        if response.status_code == 200:
            return data['token']
        if response.status_code == 400:
            raise InvalidCredentialsException("Username and password are not match together")
        if str(response.status_code).startswith('5'):
            raise Exception("API ERROR: {}".format(data))
