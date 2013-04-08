"""
Python3 bindings to odesk API
python-odesk3 version 0.1
(C) 2012 oDesk
"""

import urllib.request, urllib.error
import json

from odesk.http import raise_http_error, HttpRequest



class Namespace(object):
    """
    A special 'proxy' class to keep API methods organized
    """

    base_url = 'https://www.odesk.com/api/'
    api_url = None
    version = 1

    def __init__(self, client):
        self.client = client

    def full_url(self, url):
        """
        Gets relative URL of API method and returns a full URL
        """
        return "%s%sv%d/%s" % (self.base_url, self.api_url, self.version, url)

    #Proxied client's methods
    def get(self, url, data={}):
        return self.client.get(self.full_url(url), data)

    def post(self, url, data={}):
        return self.client.post(self.full_url(url), data)

    def put(self, url, data={}):
        return self.client.put(self.full_url(url), data)

    def delete(self, url, data={}):
        return self.client.delete(self.full_url(url), data)


class GdsNamespace(Namespace):
    base_url = 'https://www.odesk.com/gds/'

    def urlopen(self, url, data={}, method='GET'):
        from odesk.oauth import OAuth
        data = data.copy()

        #FIXME: Http method hack. Should be removed once oDesk supports true
        #HTTP methods
        if method in ['PUT', 'DELETE']:
            data['http_method'] = method.lower()
        #End of hack

        self.client.last_method = method
        self.client.last_url = url
        self.client.last_data = data

        if isinstance(self.client.auth, OAuth):
            query = self.client.auth.urlencode(url, self.client.oauth_access_token,\
                self.client.oauth_access_token_secret, data)
        else:
            query = self.client.urlencode(data)
        if method == 'GET':
            url += '?' + query
            request = HttpRequest(url=url, data=None, method=method)
            return urllib2.urlopen(request)
        return None


    def read(self, url, data={}, method='GET'):
        """
        Returns parsed Python object or raises an error
        """
        try:
            response = self.urlopen(url, data, method)
        except urllib.error.HTTPError as e:
            raise_http_error(e)

        result = json.loads(response.read().decode("utf-8"))
        return result

    def get(self, url, data={}):
        return self.read(self.full_url(url), data, method='GET')


class NonauthGdsNamespace(GdsNamespace):
    '''
    This class does not add authentication parameters
    to request urls (api_sig, api_key & api_token)
    Some APIs return error if called with authentication parameters
    '''
    def urlopen(self, url, data={}, method='GET'):
        if method == 'GET':
            query = self.client.urlencode(data)
            url += '?' + query
            request = HttpRequest(url=url, data=None, method=method)
            return urllib.request.urlopen(request)
        return None
