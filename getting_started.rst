.. _getting_started:


***************
Getting started
***************

..
.. _requirements:

Requirements
-----------------
You need to install oauth2 to run the python-odesk3, and mock and nosetests if you plan to develop python-odesk and/or run library's tests.

Oauth2(for python3)::
    pip install -e https://github.com/hades/python-oauth2/tarball/python3#egg=oauth2

Mock::

    pip install mock
    #or
    easy_install mock

Nosetests::

    pip install nose
    #or
    easy_install nose

.. _install:

Install
-----------------
On most UNIX-like systems, you’ll probably need to run these commands as root or using sudo.

To install::

    python setup.py install


Also, you can retrieve fresh version of python-odesk from GitHub::

    git clone git://github.com/vihtinsky/python-odesk3.git

.. _settings:

Settings
---------------------

You will need to use your public and private oDesk API keys::

    client = odesk.Client('your public key', 'your secret key')

To get oDesk API keys, please visit the http://www.odesk.com/services/api/keys

.. _simple_example:

Simple example
---------------------
Some examples of using listed in the odesk/examples folder.
Here is the simple example.

Initializing the client::

    client = odesk.Client(public_key, secret_key)

Shows the url to get frob from it after app authorization on odesk and getting redirect to callback::

    print client.auth.auth_url()

Waiting for inputing the frob::

    print "After that you should be redirected back to your app URL with " + \
          "additional ?frob= parameter"
    frob = raw_input('Enter frob: ')

Authentication::

    auth_token, user = client.auth.get_token(frob)
    print "Authenticated user:"
    print user

Installation of new client already with token::

    client = odesk.Client(public_key, secret_key, auth_token)

Getting user's teamrooms::

    print client.team.get_teamrooms()
