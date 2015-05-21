from ..resource import Resource
import requests
import pydash
import json

# Transactions
# This class provides methods for dealing with transactions
class Users(Resource):
    """Class encapsulating functionality relating to etsy users
    Derives from class Resource
    """
    def __init__(self, creds):
        Resource.__init__(self, creds)

    # Get transactions for the given shop
    def me(self):
        """Gets the currently auth'd user

        returns:
        dict
        """
        params = { 'includes': 'Shops/Sections' }
        resource = 'users/__SELF__'
        results = self.get(resource, params=params)
        return results

    def get_feedback(self, scope_to='as-seller'):
        """Gets the feedback associated with the current sellerFeedback

        return:
        dict
        """

        params = { 'includes': 'User' }
        resource = 'users/__SELF__/feedback/' + scope_to
        results = self.get(resource, params=params)
        return results