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
    @mock.patch('petsy.resource.Resource.get_auth', return_value='auth')
    def test_get(self, patched, patched2):
        r = Resource(self.creds)
        
        resp = r.get('some/resource', params={ 'q': 'test' })
        assert resp == {
          'data': [],
            'meta': {
                'count': 0,
                'type': 'item'
            }
        }

        # Test that get is called with the params that were passed in
        # (base uri + resource)
        patched2.assert_called_with('https://openapi.etsy.com/v2/some/resource', params={ 'q': 'test' }, auth='auth')

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: r.get(None))

    @mock.patch('requests.get', return_value=MockResponse())
    @mock.patch('petsy.resource.Resource.get_auth', return_value='auth')
    def test_scan(self, patched, patched2):
        r = Resource(self.creds)
        
        resp = r.scan('some/resource', params={ 'q': 'test' })
        assert resp == {
          'data': [],
            'meta': {
                'count': 0,
                'type': 'item'
            }
        }

        # Test that get is called with the params that were passed in
        # (base uri + resource)
        patched2.assert_called_with('https://openapi.etsy.com/v2/some/resource', params={'offset': -1, 'q': 'test', 'limit': 100}, auth='auth')

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: r.scan(None))
        