import unittest
from unittest import mock
from petsy.listings.api import Listings

class Creds(object):
    pass

class TestListings(unittest.TestCase):
    def setUp(self):
        creds = Creds()
        creds.consumer_key = 'key'
        creds.consumer_secret = 'secret'
        creds.access_token = 'token'
        creds.access_token_secret = 'token_secret'
        self.creds = creds

    def tearDown(self):
        pass

    @mock.patch('petsy.listings.api.Listings.scan', return_value={ 'data':[] })
    def test_get_listings(self, patched):
        t = Listings(self.creds)
        
        # patched method should be called with correct args
        assert t.get_listings('davepollotart') == { 'data': [] }
        patched.assert_called_with('shops/davepollotart/listings/active', params={ 'includes': 'Images' })

        # patched method should be called with correct args when non-default status is supplied
        assert t.get_listings('davepollotart', status='inactive') == { 'data': [] }
        patched.assert_called_with('shops/davepollotart/listings/inactive', params={ 'includes': 'Images' })

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: t.get_listings(None))

    @mock.patch('petsy.listings.api.Listings.get', return_value={ 'data': [] })
    def test_get_listing(self, patched):
        t = Listings(self.creds)

        # patched method should be called with correct args
        assert t.get_listing('1234') == { 'data': [] }
        patched.assert_called_with('listings/1234', params={ 'includes': 'Variations' })

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: t.get_listings(None))

    @mock.patch('petsy.listings.api.Listings.get', return_value={ 'data': [] })
    def test_get_variations(self, patched):
        t = Listings(self.creds)

        # patched method should be called with correct args
        assert t.get_variations('1234') == { 'data': [] }
        patched.assert_called_with('listings/1234/variations')

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: t.get_variations(None))

if __name__ == '__main__':
    unittest.main()