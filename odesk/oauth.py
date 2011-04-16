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

#import oauth2 as oauth

try:
    import json
except ImportError:
    import simplejson as json


from odesk.exceptions import *
from odesk.namespaces import *


class OAuth(Namespace):
    pass
