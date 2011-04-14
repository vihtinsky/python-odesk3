"""
Python bindings to odesk API
python-odesk version 0.4
(C) 2010-2011 oDesk
"""

import cookielib
from datetime import date
import hashlib
import logging
import urllib
import urllib2


try:
    import json
except ImportError:
    import simplejson as json

from odesk.exceptions import *
from odesk.namespaces import *


def signed_urlencode(secret, query={}):
    """
    Converts a mapping object to signed url query

    >>> signed_urlencode('some$ecret', {})
    'api_sig=5da1f8922171fbeffff953b773bcdc7f'
    >>> signed_urlencode('some$ecret', {'spam':42,'foo':'bar'})
    'api_sig=11b1fc2e6555297bdc144aed0a5e641c&foo=bar&spam=42'
    """
    message = secret
    for key in sorted(query.keys()):
        message += _utf8_str(key) + _utf8_str(query[key])
    #query = query.copy()
    _query = {}
    _query['api_sig'] = hashlib.md5(message).hexdigest()
    for k, v in query.iteritems():
        _query[_utf8_str(k)] = _utf8_str(v)
    return urllib.urlencode(_query)



class Auth(Namespace):

    api_url = 'auth/'
    version = 1

    def auth_url(self, frob=None):
        """
        Returns authentication URL to be used in a browser
        In case of desktop (non-web) application a frob is required
        """
        data = {}
        if frob:
            data['frob'] = frob
        url = 'https://www.odesk.com/services/api/auth/?' + \
            self.client.urlencode(data)
        return url

    def get_frob(self):
        """
        Gets the frob for authentication
        """
        url = 'keys/frobs'
        result = self.post(url)
        return result['frob']

    def get_token(self, frob):
        """
        Gets authentication token
        """
        url = 'keys/tokens'
        result = self.post(url, {'frob': frob})
        #TODO: Maybe there's a better way to get user's info?
        return result['token'], result['auth_user']

    def check_token(self):
        """
        Check validity of authentication token
        """
        url = 'keys/token'
        result = self.get(url)
        return result['token'], result['auth_user']

    def revoke_token(self):
        """
        Revoke authentication token
        """
        url = 'keys/token'
        data = {'api_token': self.client.api_token,
                'api_key': self.client.public_key}
        return self.delete(url, data)

