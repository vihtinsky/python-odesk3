"""
Python bindings to odesk API
python-odesk version 0.1
(C) 2010 oDesk
"""
import odesk
from datetime import datetime

PUBLIC_KEY = None
SECRET_KEY = None

#TODO: Desktop app example (check if it's working at all - wasn't last time)

def time_reports(public_key, secret_key):
    print "Emulating web-based app"
    #Instantiating a client without an auth token
    client = odesk.Client(public_key, secret_key)
    print "Please to this URL (authorize the app if necessary):"
    print client.auth.auth_url()
    print "After that you should be redirected back to your app URL with " + \
          "additional ?frob= parameter"
    frob = raw_input('Enter frob: ') 
    auth_token, user = client.auth.get_token(frob)
    print "Authenticated user:"
    print user
    #Instantiating a new client, now with a token. 
    #Not strictly necessary here (could just set `client.auth_token`), but 
    #typical for web apps, which wouldn't probably keep client instances 
    #between requests
    client = odesk.Client(public_key, secret_key, auth_token)
    # get skills
    print client.provider.get_skills('~~0c47747db0d04b5f')
    # add new skill
    client.provider.add_skill('~~0c47747db0d04b5f', {'skill':'skill'})
    # update a skill by giving a skill_id and new data
    client.provider.update_skill('~~0c47747db0d04b5f', 123, {'skill':'skill'})
    # delete a skill by giving a skill_id
    client.provider.delete_skill('~~0c47747db0d04b5f', 123)
    # get quickinfo
    print client.provider.get_quickinfo('~~0c47747db0d04b5f')
    # update a quickinfo by giving new data
    client.provider.update_quickinfo('~~0c47747db0d04b5f', {'skill':'skill'})
    # get affiliate profile
    print client.provider.get_affiliates('47325228f2f84188')
    print "Revoke access"
    print client.auth.revoke_token()    
    
 
if __name__ == '__main__':
    public_key = PUBLIC_KEY or raw_input('Enter public key: ')
    secret_key = SECRET_KEY or raw_input('Enter secret key: ')

    time_reports(public_key, secret_key)

