import requests
from requests_oauthlib import OAuth1
from util.objectdict import ObjectView
from petsy.listings.api import Listings
from petsy.transactions.api import Transactions
from petsy.shops.api import Shops

BASE_URI = 'https://openapi.etsy.com/v2/'

# Class to hold credentials
class Credentials(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

class Api(object):
    def __init__(self, **kwargs):
        creds = Credentials(
            kwargs['consumer_key'],
            kwargs['consumer_secret'],
            kwargs['access_token'],
            kwargs['access_token_secret']
        )
        self.listings = Listings(creds)
        self.transactions = Transactions(creds)
        self.shops = Shops(creds)
