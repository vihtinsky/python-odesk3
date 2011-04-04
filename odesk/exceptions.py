"""
Python bindings to odesk API
python-odesk version 0.4
(C) 2010-2011 oDesk
"""

import logging
import urllib2


class HTTP400BadRequestError(urllib2.HTTPError):
    pass


class HTTP401UnauthorizedError(urllib2.HTTPError):
    pass


class HTTP403ForbiddenError(urllib2.HTTPError):
    pass


class HTTP404NotFoundError(urllib2.HTTPError):
    pass


class InvalidConfiguredException(Exception):
    pass


class APINotImplementedException(Exception):
    pass


class AuthenticationError(Exception):
    pass


class NotAuthenticatedError(Exception):
    pass
