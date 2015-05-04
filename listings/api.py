
from petsy.resource import Resource
import requests
import pydash
import json

# Listings
# This class provides methods for dealing with listings
class Listings(Resource):
    """Class encapsulating functionality relating to etsy listings
    Derives from class Resource
    """
    def __init__(self, creds):
        Resource.__init__(self, creds)

    # Get listings for the given shop
    def get_listings(self, shop_id, status='active'):
        """Gets the listings for the for the given shop and status
        Arguments:
        shop_id -- The id of the shop to pull listings for
        status -- The status to filter results by, defaults to 'active'

        Returns:
        dict
        """
        assert shop_id != None, 'Expected shop_id to be a non null string.'
        params = { 'includes': 'Images' }
        url = 'shops/' + shop_id + '/listings/' + status
        return self.scan(url, params=params)

    # Get the given listing
    def get_listing(self, listing_id):
        """Gets the listing with the given id
        Arguments:
        listing_id -- The id of the listing to pull

        Returns:
        dict
        """
        assert listing_id != None, 'Expected listing_id to be a non null string.'
        params = { 'includes': 'Variations' }
        url = 'listings/' + listing_id
        return self.get(url, params=params)

    # Get the variations for the given listing_id
    def get_variations(self, listing_id):
        """Gets the variations associated with the given listing
        Arguments:
        listing_id -- The id of the listing for which to pull variations

        Returns: dict
        """
        assert listing_id != None, 'Expected listing_id to be a non null string.'
        url = 'listings/' + listing_id + '/variations'
        return self.get(url)

