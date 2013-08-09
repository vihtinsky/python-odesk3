"""
Python3 bindings to odesk API
python-odesk3 version 0.1
(C) 2012 oDesk
"""

import time
import urlparse, urllib
import oauth2 as oauth


from odesk.namespaces import Namespace


class OAuth(Namespace):
    """
    oAuth support in oDesk is in beta currently.
    """

    api_url = 'auth/'
    version = 1

    request_token_url = 'https://www.odesk.com/api/auth/v1/oauth/token/request'
    authorize_url = 'https://www.odesk.com/services/api/auth'
    access_token_url = 'https://www.odesk.com/api/auth/v1/oauth/token/access'

    def urlencode(self, url, key, secret, data={}, method='GET'):
        """
        Converts a mapping object to signed url query
        """
        token = oauth.Token(key, secret)
        consumer = self.get_oauth_consumer()
        data.update({
            'oauth_token': token.key,
            'oauth_consumer_key': consumer.key,
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
        })
        request = oauth.Request(method=method, url=url, parameters=data)
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method, consumer, token)
        return request.to_postdata()

    def get_oauth_consumer(self):
        """
        Returns OAuth consumer object
        """
        return oauth.Consumer(self.client.public_key, self.client.secret_key)

    def get_request_token(self):
        """
        Returns request token and request token secret
        """
        client = oauth.Client(self.get_oauth_consumer())
        #import pdb
        #pdb.set_trace()
        response, content = client.request(self.request_token_url, 'POST')
        if response.get('status') != '200':
            raise Exception("Invalid request token response: %s." % content)
        request_token = dict(urlparse.parse_qsl(content))
        self.request_token = request_token.get(b'oauth_token')
        self.request_token_secret = request_token.get(b'oauth_token_secret')
        return self.request_token, self.request_token_secret

    def get_authorize_url(self, callback_url=None):
        """
        Returns authentication URL to be used in a browser
        """
        oauth_token = getattr(self, 'request_token', None) or\
            self.get_request_token()[0]
        if callback_url:
            params = urllib.urlencode({'oauth_token': oauth_token,\
                'oauth_callback': callback_url})
        else:
            params = urllib.urlencode({'oauth_token': oauth_token})
        return '%s?%s' % (self.authorize_url, params)

    def get_access_token(self, verifier):
        """
        Returns access token and access token secret
        """
        try:
            request_token = self.request_token
            request_token_secret = self.request_token_secret
        except AttributeError:
            raise Exception("At first you need to call get_authorize_url")
        token = oauth.Token(request_token, request_token_secret)
        token.set_verifier(verifier)
        client = oauth.Client(self.get_oauth_consumer(), token)
        response, content = client.request(self.access_token_url, 'POST')
        if response.get('status') != '200':
            raise Exception("Invalid access token response: %s." % content)
        access_token = dict(urlparse.parse_qsl(content))
        self.access_token = access_token.get(b'oauth_token')
        self.access_token_secret = access_token.get(b'oauth_token_secret')
        return self.access_token, self.access_token_secret
