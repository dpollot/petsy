
from ..resource import Resource
import requests
import pydash
import json

# Shops
# This class provides methods for dealing with shops
class Shops(Resource):
    """Class encapsulating functionality relating to etsy shops
    Derives from class Resource
    """
    def __init__(self, creds):
        Resource.__init__(self, creds)

    # Get the given shop
    def get_shop(self, shop_id):
        """Gets the shop associated with the given shop_id
        arguments:
        shop_id -- The id of the shop to get

        returns:
        dict
        """
        assert shop_id != None, 'Expected shop_id to be a non null string'
        params = { 'includes': 'User,About,Sections' }
        resource = 'shops/' + shop_id
        return self.get(resource, params=params)