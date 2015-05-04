
from util.objectdict import ObjectView
from requests_oauthlib import OAuth1
import json
from collections import namedtuple
import requests

# Base class for resources
class Resource(object):
    # constructor
    # creds: 
    #   consumer_key
    #   consumer_secret
    #   access_token
    #   access_token_secret
    def __init__(self, creds):
        self.consumer_key = creds.consumer_key
        self.consumer_secret = creds.consumer_secret
        self.access_token = creds.access_token
        self.access_token_secret = creds.access_token_secret
        self.BASE_URI = 'https://openapi.etsy.com/v2/'

    # Returns an auth object to be used within requests
    def get_auth(self):
        """Get an OAuth1 object based on current credentials
        """
        return OAuth1(
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret
        )

    # Get the resource (paged)
    def get(self, resource, params=None):
        """Get the given resource

        Arguments:
        resource -- The resource (url, less query params) to get
        params   -- Query params

        Returns:
        A dictionary containing the results of the get request
        """
        assert resource != None, 'expected resource to be a non null string'
        assert len(resource) > 0

        auth = self.get_auth()
        url = self.BASE_URI + resource

        resp = requests.get(url, auth=auth, params=params)
        if resp.status_code != 200:
            return {
                'errors': [resp.text],
                'status': resp.status_code
            }

        r = resp.json()
        return {
            'data': r['results'],
            'meta': {
                'count': r['count'],
                'type': r['type']
            }
        }

    # Get all items of a given resource type
    def scan(self, resource, params=None):
        """Iterates through an entire paged resource collection

        Arguments:
        resource -- The resource to get
        params   -- (Optional) query params

        Returns:
        dict containing the results of the request
        """
        assert resource != None, 'expected resource to be a non null string'
        assert len(resource) > 0

        query = params if params != None else {}
        query['limit'] = 100
        query['offset'] = 0

        auth = self.get_auth()
        url = self.BASE_URI + resource
        
        results = []
        count = 0
        resource_type = ''

        while query['offset'] > -1:
            resp = requests.get(url, auth=auth, params=query)
            if resp.status_code != 200:
                return {
                    'status': resp.status_code,
                    'errors': [resp.text]
                }

            r = resp.json()

            # save the count for later
            count = r['count']
            resource_type = r['type']

            for item in r['results']:
                results.append(item)

            query['offset'] = -1 if 'pagination' not in r or r['pagination'] == None \
                or r['pagination']['next_page'] == None \
                else int(r['pagination']['next_offset'])
        
        return {
            'data':results,
            'meta': {
                'count': count,
                'type': resource_type
            }
        }
