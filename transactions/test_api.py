import unittest
from unittest import mock
from petsy.transactions.api import Transactions

class Creds(object):
    pass

class TestTransactions(unittest.TestCase):
    def setUp(self):
        creds = Creds()
        creds.consumer_key = 'key'
        creds.consumer_secret = 'secret'
        creds.access_token = 'token'
        creds.access_token_secret = 'token_secret'
        self.creds = creds

    def tearDown(self):
        pass

    @mock.patch('petsy.transactions.api.Transactions.get', return_value={ 'data':[] })
    def test_get_transactions(self, patched):
        t = Transactions(self.creds)
        
        # patched method should be called with correct args
        assert t.get_transactions('davepollotart') == { 'data': [] }
        patched.assert_called_with('shops/davepollotart/transactions', params={ 'includes': 'Listing' })

        # tested method raise an error if invalid arguments are passed in
        self.assertRaises(AssertionError, lambda: t.get_transactions(None))

    @mock.patch('petsy.transactions.api.Transactions.get', return_value={ 'data':[] })
    def test_get_listing_transactions(self, patched):
        t = Transactions(self.creds)
        
        # patched method should be called with correct args
        assert t.get_listing_transactions('listingid') == { 'data': [] }
        patched.assert_called_with('listings/listingid/transactions', params={ 'includes': 'Listing' })

        # tested method should raise an error if invalid argumets are supplied
        self.assertRaises(AssertionError, lambda: t.get_listing_transactions(None))

if __name__ == '__main__':
    unittest.main()