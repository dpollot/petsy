import unittest
from unittest import mock
from petsy.resource import Resource
import requests

class MockResponse(object):
    def __init__(self):
        self.status_code = 200
        self.text = '{"results":[]"}'

    def json(self):
        return {
            'results': [],
            'count': 0,
            'type': 'item'
        }

class Creds(object):
    pass

class TestResource(unittest.TestCase):
    def setUp(self):
        creds = Creds()
        creds.consumer_key = 'key'
        creds.consumer_secret = 'secret'
        creds.access_token = 'token'
        creds.access_token_secret = 'token_secret'
        self.creds = creds

    def tearDown(self):
        pass

    def test_get_auth(self):
        auth = Resource(self.creds).get_auth()
        assert auth.client.client_key == 'key'
        assert auth.client.client_secret == 'secret'
        assert auth.client.resource_owner_key == 'token'
        assert auth.client.resource_owner_secret == 'token_secret'

    @mock.patch('requests.get', return_value=MockResponse())
    def test_get(self, patched):
        r = Resource(self.creds)
        resp = r.get('some/resource', params={ 'q': 'test' })
        assert resp == {
          'data': [],
            'meta': {
                'count': 0,
                'type': 'item'
            }
        }

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: r.get(None))

    def test_scan(self):
        pass