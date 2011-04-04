"""
Python bindings to odesk API
python-odesk version 0.4
(C) 2010-2011 oDesk
"""

import cookielib
from datetime import date
import time
import hashlib
import logging
import urllib
import urllib2

import oauth2 as oauth

try:
    import json
except ImportError:
    import simplejson as json


from odesk.exceptions import *
from odesk.namespace import *


class OAuth(Namespace):

    oauth_request_url = 'https://www.odesk.com/api/auth/v1/oauth/token/request'
    oauth_auth_user_url ='https://www.odesk.com/services/api/auth'
    oauth_access_url = 'https://www.odesk.com/api/auth/v1/oauth/token/access'
    
    key = ''
    secret = ''
    
    

    def sign_request(self, url, key, secret, method='GET', params=None):
        oauth_params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time())
        }
        
        if params:
            for param in params.keys():
                oauth_params[param] = params[param]
            
        token = oauth.Token(key, secret)
        consumer = oauth.Consumer(key, secret)

        oauth_params['oauth_token'] = token.key
        oauth_params['oauth_consumer_key'] = consumer.key

        req = oauth.Request(method=method, url=url,
                            parameters=oauth_params)

        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, consumer, token)
        
        return req


    def get_request_token(self, key, secret):
        consumer = oauth.Consumer(key, secret)
        client = oauth.Client(consumer)
        resp, content = client.request(self.oauth_request_url, "POST")
        print resp
        print content
        return client
