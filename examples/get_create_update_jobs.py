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

def hr_post_job(public_key, secret_key):
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
    job_data = {
                'buyer_team_reference': 111,
                'title': 'Test job from API',
                'job_type': 'hourly',
                'description': 'this is test job, please do not apply to it',
                'visibility': 'odesk',
                'duration': 10,
                'category': 'Web Development',
                'subcategory': 'Other - Web Development',
                }
    try:
        print(client.hr.post_job(job_data))
    except Exception as e:
        print("Exception at %s %s" % (client.last_method, client.last_url))
        raise e


    
 
if __name__ == '__main__':
    public_key = PUBLIC_KEY or input('Enter public key: ')
    secret_key = SECRET_KEY or input('Enter secret key: ')

    hr_post_job(public_key, secret_key)

