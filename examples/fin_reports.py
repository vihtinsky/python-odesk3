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

def fin_reports(public_key, secret_key):
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
    print(client.finreport.get_provider_billings('11111',
                    odesk.utils.Query(select=['date', 'type',
                                        'amount'],
                    where=((odesk.utils.Q('date') <= date.today())))))


if __name__ == '__main__':
    public_key = PUBLIC_KEY or input('Enter public key: ')
    secret_key = SECRET_KEY or input('Enter secret key: ')

    fin_reports(public_key, secret_key)

