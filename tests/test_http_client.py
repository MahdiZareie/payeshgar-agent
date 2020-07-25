from unittest import TestCase, mock

from payeshgar_agent.payeshgar_http_client.v1.auth import JWTAuthentication
from payeshgar_agent.payeshgar_http_client.v1.client import PayeshgarServerHTTPClient
from payeshgar_agent.payeshgar_http_client.v1.session import HttpSessionBuilder

CREDENTIALS = {"username": "foo", "password": "bar"}
TOKEN = "IAMJWTTOKEN"


def mocked_request(status_code=200, exception=None):
    def _(*args, **kwargs):
        if exception:
            raise exception
        sample_response = mock.MagicMock(status_code=status_code)
        sample_response.json.return_value = dict(token=TOKEN)
        return sample_response

    return _


class JWTAuthenticationTestCase(TestCase):

    def test_authenticate_should_correctly_set_headers(self):
        mocked_session = mock.MagicMock(headers={})
        mocked_session.post.side_effect = mocked_request()

        sut = JWTAuthentication(credentials=CREDENTIALS)
        sut.authenticate(mocked_session)

        self.assertEquals(mocked_session.headers['AUTHORIZATION'], '{} {}'.format(sut.auth_header_prefix, TOKEN))

    def test_authenticate_should_retry_in_case_of_non_4xx_http_errors(self):
        mocked_session = mock.MagicMock(headers={})
        mocked_session.post.side_effect = mocked_request(status_code=502)
        expected_retry = 10
        sut = JWTAuthentication(credentials=CREDENTIALS, retry_on_failure=expected_retry)
        with self.assertRaises(Exception):
            sut.authenticate(mocked_session)
        self.assertEquals(mocked_session.post.call_count, expected_retry)

    def test_authenticate_should_not_retry_in_case_of_4xx_http_errors(self):
        mocked_session = mock.MagicMock(headers={})
        mocked_session.post.side_effect = mocked_request(status_code=400)
        expected_retry = 1
        sut = JWTAuthentication(credentials=CREDENTIALS, retry_on_failure=expected_retry + 10)
        with self.assertRaises(Exception):
            sut.authenticate(mocked_session)
        self.assertEquals(mocked_session.post.call_count, expected_retry)


class HttpSessionBuilderTestCase(TestCase):
    def test_builder_should_apply_authentcate_on_session(self):
        mocked_auth = mock.Mock()

        session = HttpSessionBuilder().authentication(mocked_auth).build()

        mocked_auth.authenticate.assert_called_once_with(session)

    def test_builder_should_correctly_set_timeout(self):
        expected_timeout = 77
        session = HttpSessionBuilder().api_timeout(expected_timeout).build()

        self.assertEquals(session.timeout, expected_timeout)

    def test_builder_should_correctly_set_url_prefix(self):
        base = "https://somewhere.someserver.tld/somegateway"
        prefix = "/payeshgar/v1/"
        expected = "https://somewhere.someserver.tld/somegateway/payeshgar/v1/"
        session = HttpSessionBuilder().base_url(base).url_prefix(prefix).build()

        self.assertEquals(session.base_url, expected)


