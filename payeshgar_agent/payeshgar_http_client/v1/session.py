from typing import Union
from urllib.parse import urljoin

import requests


class SimpleSession(requests.Session):
    def __init__(self, base_url: str, timeout: float):
        self.base_url = base_url
        super(SimpleSession, self).__init__()
        self.headers['content-type'] = "application/json"
        self.timeout = timeout

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        kwargs.setdefault('timeout', self.timeout)
        url = self.create_url(url)
        return super(SimpleSession, self).request(
            method, url, *args, **kwargs
        )

    def create_url(self, url: str):
        """Create the URL based off this partial path."""
        return "{}/{}".format(self.base_url, url.lstrip("/"))


class HttpSessionBuilder:
    def __init__(self):
        self._session_provider = SimpleSession
        self._url_prefix = ""
        self._base_url = ""
        self._auth = None
        self._api_timeout = 5

    def api_timeout(self, timeout: Union[int, float]):
        self._api_timeout = timeout
        return self

    def authentication(self, auth):
        self._auth = auth
        return self

    def base_url(self, base_url):
        self._base_url = base_url.rstrip("/")
        return self

    def url_prefix(self, url_prefix: str):
        self._url_prefix = url_prefix.strip('/')
        return self

    def session_provider(self, session_provider):
        self._session_provider = session_provider
        return self

    def build(self) -> SimpleSession:
        session = self._session_provider(
            base_url="{}/{}/".format(self._base_url, self._url_prefix),
            timeout=self._api_timeout
        )
        if self._auth is not None:
            self._auth.authenticate(session)
        return session
