import unittest
from unittest import mock
from petsy.shops.api import Shops

class Creds(object):
    pass

class TestShops(unittest.TestCase):
    def setUp(self):
        creds = Creds()
        creds.consumer_key = 'key'
        creds.consumer_secret = 'secret'
        creds.access_token = 'token'
        creds.access_token_secret = 'token_secret'
        self.creds = creds

    def tearDown(self):
        pass

    @mock.patch('petsy.shops.api.Shops.get', return_value={ 'data':[] })
    def test_get_shop(self, patched):
        t = Shops(self.creds)
        
        # patched method should be called with correct args
        assert t.get_shop('davepollotart') == { 'data': [] }
        patched.assert_called_with('shops/davepollotart', params={ 'includes': 'User,About,Sections' })

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: t.get_shop(None))

if __name__ == '__main__':
    unittest.main()