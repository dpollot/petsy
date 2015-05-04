
from ..resource import Resource
import requests
import pydash
import json

# Transactions
# This class provides methods for dealing with transactions
class Transactions(Resource):
    """Class encapsulating functionality relating to etsy transactions
    Derives from class Resource
    """
    def __init__(self, creds):
        Resource.__init__(self, creds)

    # Get transactions for the given shop
    def get_transactions(self, shop_id):
        """Gets the transactions for the given shop
        arguments:
        shop_id -- the id of the shop to pull transactions for

        returns:
        dict
        """
        assert shop_id != None, 'Expected shop_id to be a non null string.'
        params = { 'includes': 'Listing' }
        resource = 'shops/' + shop_id + '/transactions'
        results = self.get(resource, params=params)
        return results

    # Get all transactions for the given shop and listing
    def get_listing_transactions(self, listing_id):
        """Gets the transactions for the given listing
        arguments:
        listing_id -- the id of the listings to pull transactions for

        returns:
        dict
        """
        assert listing_id != None, 'Expected listing_id to be a non null string.'
        params = { 'includes': 'Listing' }
        resource = 'listings/' + listing_id  + '/transactions'
        return self.get(resource, params=params)