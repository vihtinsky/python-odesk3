"""
Python3 bindings to odesk API
python-odesk3 version 0.1
(C) 2012 oDesk
"""

import urllib2

from odesk.exceptions import (HTTP400BadRequestError, HTTP401UnauthorizedError,
    HTTP403ForbiddenError, HTTP404NotFoundError)


def raise_http_error(e):
    '''Raise custom exception'''
    if e.code == 400:
        raise HTTP400BadRequestError(e.filename, e.code, e.msg,
                                     e.hdrs, None)
    elif e.code == 401:
        raise HTTP401UnauthorizedError(e.filename, e.code, e.msg,
                                       e.hdrs, None)
    elif e.code == 403:
        raise HTTP403ForbiddenError(e.filename, e.code, e.msg,
                                    e.hdrs, None)
    elif e.code == 404:
        raise HTTP404NotFoundError(e.filename, e.code, e.msg,
                                   e.hdrs, None)
    else:
        raise e


class HttpRequest(urllib2.Request):
    """
    A hack around Request class that allows to specify HTTP method explicitly
    """

    def __init__(self, *args, **kwargs):
        #Request is an old-style class, so can't use `super`
        method = kwargs.pop('method', 'GET')
        urllib2.Request.__init__(self, *args, **kwargs)
        self.method = method

    def get_method(self):
        #FIXME: Http method hack. Should be removed once oDesk supports true
        #HTTP methods
        if self.method in ['PUT', 'DELETE']:
            return 'POST'
        #End of hack

        return self.method
