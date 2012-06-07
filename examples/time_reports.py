"""
Python bindings to odesk API
python-odesk version 0.1
(C) 2010 oDesk
"""
import odesk
import odesk.utils
from datetime import date

PUBLIC_KEY = None
SECRET_KEY = None

#TODO: Desktop app example (check if it's working at all - wasn't last time)

def time_reports(public_key, secret_key):
    print("Emulating web-based app")
    #Instantiating a client without an auth token
    client = odesk.Client(public_key, secret_key)
    print("Please to this URL (authorize the app if necessary):")
    print(client.auth.auth_url())
    print("After that you should be redirected back to your app URL with " + \
          "additional ?frob= parameter")
    frob = input('Enter frob: ')
    auth_token, user = client.auth.get_token(frob)
    print("Authenticated user:")
    print(user)
    #Instantiating a new client, now with a token.
    #Not strictly necessary here (could just set `client.auth_token`), but
    #typical for web apps, which wouldn't probably keep client instances
    #between requests
    client = odesk.Client(public_key, secret_key, auth_token)
    print(client.timereport.get_provider_report('user1',
            odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
            where=(odesk.utils.Q('worked_on') <= date.today()) &\
             (odesk.utils.Q('worked_on') > '2012-05-01'))))

    print(client.timereport.get_provider_report('user1',
            odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
            where=(odesk.utils.Q('worked_on') <= date.today()) &\
             (odesk.utils.Q('worked_on') > '2012-05-01')), hours=True))

    print(client.timereport.get_agency_report('company1', 'agency1',
            odesk.utils.Query(select=odesk.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
            where=(odesk.utils.Q('worked_on') <= date.today()) &\
            (odesk.utils.Q('worked_on') > '2010-05-01')), hours=True))


if __name__ == '__main__':
    public_key = PUBLIC_KEY or input('Enter public key: ')
    secret_key = SECRET_KEY or input('Enter secret key: ')

    time_reports(public_key, secret_key)

