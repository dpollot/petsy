import unittest
from unittest import mock
from petsy.auth.api import EtsyAuth

# Mocked token response from oauth
request_token = {
    'oauth_token': 'oauth_token',
    'oauth_token_secret': 'oauth_token_secret'
}

# Mocked access token response from oauth
access_tokens = {
    'oauth_token': 'access_token',
    'oauth_token_secret': 'access_token_secret'
}

class MockReq(object):
    pass
class Creds(object):
    pass

class TestAuth(unittest.TestCase):
    def setUp(self):
        creds = Creds()
        creds.consumer_key = 'key'
        creds.consumer_secret = 'secret'
        creds.access_token = 'token'
        creds.access_token_secret = 'token_secret'
        self.creds = creds

        self.session = {}

    def tearDown(self):
        pass

    @mock.patch('requests_oauthlib.OAuth1Session.fetch_request_token', return_value=request_token)
    @mock.patch('requests_oauthlib.OAuth1Session.authorization_url', return_value='secure_url')
    def test_fetch_authorization_url(self, patched1, patched2):
        auth = EtsyAuth(['transactions_r'])
        auth_url = auth.fetch_authorization_url(
            self.creds.consumer_key,
            self.creds.consumer_secret,
            'http://localhost:5000/authorize',
            self.session
        )
        assert auth_url == 'secure_url'
        assert len(self.session.keys()) == 2
        assert self.session.get('oauth_token') == 'oauth_token'
        assert self.session.get('oauth_token_secret') == 'oauth_token_secret'

    @mock.patch('requests_oauthlib.OAuth1Session.fetch_access_token', return_value=access_tokens)
    def test_handle_authorization(self, patched):
        session = {
            'oauth_token': 'oauth_token',
            'oauth_token_secret': 'oauth_token_secret'
        }
        request = MockReq()
        request.args = {
            'oauth_token': 'oauth_token',
            'oauth_verifier': 'oauth_verifier'
        }

        auth = EtsyAuth(['transactions_r'])
        auth.handle_authorization(
            self.creds.consumer_key,
            self.creds.consumer_secret,
            request,
            session
        )
        
        assert len(session.keys()) == 4
        assert session.get('access_token') == 'access_token'
        assert session.get('access_token_secret') == 'access_token_secret'

if __name__ == '__main__':
    unittest.main()