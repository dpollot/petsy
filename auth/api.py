from requests_oauthlib import OAuth1Session, OAuth1

# Provides methods that help deal with the oauth1 flow for etsy
# The class requires that you use some session to store tokens, etc.
class EtsyAuth(object):
    def __init__(self, permissions_scope):
        self.request_token_url = \
            'https://openapi.etsy.com/v2/oauth/request_token?scope=' + '%20'.join(permissions_scope)
        self.access_token_url = 'https://openapi.etsy.com/v2/oauth/access_token'
        self.authorization_base_url = 'https://www.etsy.com/oauth/signin'

    # Returns an authorization url to redirect to
    # Also saves oauth specific data into the session dictionary provided
    def fetch_authorization_url(self, consumer_key, consumer_secret, callback_uri, session):
        """Gets an authorization url that a user can be redirected to in order to auth
        Arguments:
        consumer_key    -- The client's consumer (shared) key
        consumer_secret -- The client's secret key
        callback_uri    -- The url that the etsy will redirect back to to handle auth
        session         -- A session object to store auth vars

        Returns
        string - the auth url
        """
        # Get a request token
        oauth = OAuth1Session(consumer_key,
            client_secret=consumer_secret,
            callback_uri=callback_uri)
        
        request_token_response = oauth.fetch_request_token(self.request_token_url)
        
        session['oauth_token'] = request_token_response.get('oauth_token')
        session['oauth_token_secret'] = request_token_response.get('oauth_token_secret')

        authorization_url = oauth.authorization_url(self.authorization_base_url)
        return authorization_url

    # Handles the authorization callback (after the user has authorized the app and 
    # and the oauth provider has redirected back to the app)
    def handle_authorization(self, consumer_key, consumer_secret, request, session):
        """Handles the authorization request from etsy and adds auth values to session
        Arguments:
        consumer_key    -- The client's consumer/api (shared) key
        consumer_secret -- The client's secret key
        request         -- The request object attached to the auth
        session         -- The session object
        """
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')

        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=session['oauth_token'],
            resource_owner_secret=session['oauth_token_secret'],
            verifier=oauth_verifier
        )

        oauth_tokens = oauth.fetch_access_token(self.access_token_url)
        session['access_token'] = oauth_tokens.get('oauth_token')
        session['access_token_secret'] = oauth_tokens.get('oauth_token_secret')
        